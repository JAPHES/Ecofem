# Deploying EcoFem to Vercel

This project follows Vercel's current zero-configuration Django deployment model. Vercel detects `manage.py`, reads `ASGI_APPLICATION`, installs `requirements.txt`, runs `collectstatic`, and serves collected static assets from its CDN.

The Django application itself can run as a Vercel Function, but its database and admin-uploaded media must use persistent external services. SQLite and the Vercel function filesystem must not be used for production content.

## Production architecture

```text
Browser
   |
   v
Vercel CDN --------------> collected CSS, JavaScript and static images
   |
   v
EcoFem Django ASGI Function
   |                  |
   v                  v
PostgreSQL         S3-compatible object storage
(site content)     (admin-uploaded images)
```

Recommended starting services:

- Vercel for the Django application and static assets
- Neon Postgres through the Vercel Marketplace for database content
- AWS S3, Cloudflare R2, Backblaze B2 or another S3-compatible bucket for uploaded media

## 1. Import the GitHub project

1. Sign in at <https://vercel.com/>.
2. Select **Add New > Project**.
3. Import `JAPHES/Ecofem` from GitHub.
4. Keep the root directory as the repository root (`.`).
5. Vercel should detect Django from `manage.py` and `requirements.txt`.
6. Do not set a custom Output Directory.
7. Do not add an old `/api/index.py` route or legacy rewrite configuration.

The first deployment may stop with a clear `DATABASE_URL is required on Vercel` message. This is intentional: it prevents the live site from silently using an ephemeral SQLite database.

## 2. Add persistent PostgreSQL

From the Vercel project:

1. Open **Storage** or **Marketplace**.
2. Add a Postgres provider such as **Neon**.
3. Connect it to the EcoFem project.
4. Enable it for Production and any Preview environments that need a database.
5. Confirm that the integration created a `DATABASE_URL` environment variable.

Use the provider's pooled connection URL when one is offered. Connection pooling is important for serverless applications.

## 3. Add the required environment variables

In **Project Settings > Environment Variables**, add these for Production. Add them to Preview as well if preview deployments should run fully.

```dotenv
DJANGO_SECRET_KEY=<a-long-random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.vercel.app
DJANGO_TIME_ZONE=Africa/Nairobi
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=0
SITE_URL=https://your-project-name.vercel.app
```

`DATABASE_URL` should normally be supplied by the Postgres integration rather than entered manually.

Generate a Django secret locally with:

```powershell
py -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
```

Keep `DJANGO_SECURE_HSTS_SECONDS=0` during initial verification. After HTTPS and the final domain have worked reliably, it can be increased carefully, for example to `31536000`.

## 4. Configure durable media storage

Static project assets are handled automatically by Vercel. Images uploaded later through Django admin are different: they must use durable object storage.

Create an S3 or S3-compatible bucket and add:

```dotenv
AWS_STORAGE_BUCKET_NAME=<bucket-name>
AWS_ACCESS_KEY_ID=<storage-access-key>
AWS_SECRET_ACCESS_KEY=<storage-secret-key>
AWS_S3_REGION_NAME=<region>
AWS_QUERYSTRING_AUTH=True
```

For AWS S3, `AWS_S3_ENDPOINT_URL` can remain empty. For an S3-compatible provider, also add its endpoint:

```dotenv
AWS_S3_ENDPOINT_URL=https://<provider-endpoint>
```

If the bucket is served through an approved public custom domain or CDN, add:

```dotenv
AWS_S3_CUSTOM_DOMAIN=media.example.org
AWS_QUERYSTRING_AUTH=False
```

The configured storage identity needs permission to list the bucket and read, create, update and delete objects inside the `media/` prefix. Keep credentials in Vercel environment variables only.

The site can be viewed without an object-storage bucket, but do not upload team photos, partner logos, news images or gallery images on Vercel until persistent media storage is configured. Files written to a function's local filesystem are not durable.

## 5. Redeploy

After adding the database and environment variables:

1. Open **Deployments**.
2. Select the latest deployment.
3. Choose **Redeploy**.

Alternatively, install the current Vercel CLI and deploy from PowerShell:

```powershell
npm install --global vercel@latest
vercel login
vercel link
vercel --prod
```

## 6. Apply migrations and create the administrator

Link the local repository to the Vercel project, then pull the Production environment values:

```powershell
vercel login
vercel link
vercel env pull .env.local --environment=production
```

The project loads `.env.local` automatically and Git ignores it. With the production `DATABASE_URL` available locally, run:

```powershell
py manage.py migrate
py manage.py createsuperuser
```

These commands update the external production database. Run them deliberately from the repository root where `manage.py` is located.

After creating the superuser, sign in at:

```text
https://your-project-name.vercel.app/admin/
```

## 7. Add a custom domain

After adding a domain under **Project Settings > Domains**, update the environment variables:

```dotenv
DJANGO_ALLOWED_HOSTS=.vercel.app,ecofem.example.org,www.ecofem.example.org
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.vercel.app,https://ecofem.example.org,https://www.ecofem.example.org
SITE_URL=https://ecofem.example.org
```

Redeploy after changing environment variables.

## 8. Production verification

Check the following after deployment:

- `/`, `/about/`, `/innovation/`, `/impact/`, `/team/`, `/updates/` and `/contact/` load over HTTPS
- CSS, JavaScript, the favicon and both static project images load
- `/admin/` accepts the new superuser
- a test team member can be created, edited and removed
- an uploaded test image remains available after a redeployment
- a contact form submission appears under Contact Messages
- draft updates remain private and published updates appear publicly
- the custom 404 page appears for an unknown URL
- `DJANGO_DEBUG` remains `False`

## Updating the live site

After the Vercel project is linked to GitHub, every push to `main` creates a new Production deployment:

```powershell
git add .
git commit -m "describe the change"
git push origin main
```

Run migrations again whenever a deployment includes new Django migration files.

## Troubleshooting

### `DATABASE_URL is required on Vercel`

Connect a Postgres integration to the Vercel project and make sure it is enabled for the current deployment environment.

### `DisallowedHost`

Add the deployment or custom hostname to `DJANGO_ALLOWED_HOSTS`, without `https://`.

### CSRF verification failed in admin

Add the complete HTTPS origin to `DJANGO_CSRF_TRUSTED_ORIGINS`, including `https://` but no trailing path.

### Uploaded images disappear

The deployment is still using local file storage. Configure the S3-compatible environment variables and redeploy before uploading production media.

### Static files fail during build

Do not set a custom output directory. Vercel automatically runs Django `collectstatic` because `STATIC_ROOT` is configured.

## Official references

- Vercel Django deployment: <https://vercel.com/docs/frameworks/full-stack/django>
- Vercel Python runtime: <https://vercel.com/docs/functions/runtimes/python>
- Vercel storage marketplace: <https://vercel.com/docs/marketplace-storage>
- Django deployment checklist: <https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/>
- django-storages S3 backend: <https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html>
