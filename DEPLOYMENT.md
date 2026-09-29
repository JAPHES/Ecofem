# Deploying EcoFem to Vercel

EcoFem is configured as a database-free Django website. Vercel runs the Django
ASGI application and serves its collected static files from the CDN. No
database, migrations, Django admin, media upload service or object-storage
integration is required.

## 1. Import the GitHub project

1. Sign in at <https://vercel.com/>.
2. Select **Add New → Project**.
3. Import `JAPHES/Ecofem` from GitHub.
4. Keep the Root Directory as the repository root (`.`).
5. Let Vercel detect Django from `manage.py`.
6. Leave Build Command and Output Directory unchanged.

Do not add a Postgres integration, `DATABASE_URL`, S3 bucket, Blob store or
other storage product for this version.

## 2. Configure environment variables

Under **Project Settings → Environment Variables**, add:

```dotenv
DJANGO_SECRET_KEY=<a-long-random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app,ecofem.secora.dev
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.vercel.app,https://ecofem.secora.dev
DJANGO_TIME_ZONE=Africa/Nairobi
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=0
SITE_URL=https://ecofem.secora.dev
```

Generate a secret locally with:

```powershell
py -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
```

Keep the value private. Do not add it to Git or `ecofem/content.py`.

## 3. Deploy

Click **Deploy**. The temporary `vercel.app` address can be used to verify the
deployment before connecting `ecofem.secora.dev`.

No migration or superuser commands are needed.

## 4. Connect `ecofem.secora.dev`

### Add the hostname to Vercel first

1. Open the EcoFem project in Vercel.
2. Select **Settings**, then **Domains**.
3. Select **Add Domain**.
4. Enter `ecofem.secora.dev` and confirm.
5. Vercel will show the exact CNAME target assigned to the project. Copy that
   value exactly. A current general-purpose value is
   `cname.vercel-dns-0.com`, but use the project-specific value shown in your
   Vercel dashboard if it is different.

### Create the record at Name.com

These steps assume `secora.dev` uses Name.com's nameservers. If Name.com shows
a nameserver warning, create the record with the DNS provider named in the
domain's current nameservers instead.

1. Sign in to Name.com.
2. Open **My Domains** and select `secora.dev`.
3. Open **Manage DNS Records**.
4. Check for an existing `ecofem` A, AAAA or CNAME record. Do not create a
   second conflicting record; remove or replace only the conflicting `ecofem`
   record.
5. Add this record using the exact target supplied by Vercel:

| Name.com field | Value |
|---|---|
| Type | `CNAME` |
| Host | `ecofem` |
| Answer | the exact Vercel CNAME target |
| TTL | `300` (default) |

Use only `ecofem` in the Host field, not the full domain, and do not enter
`https://` or a URL path in the Answer field. This CNAME does not affect the
existing `secora.dev` website or its email records.

### Verify and activate HTTPS

Return to **Vercel > EcoFem > Settings > Domains** and refresh the domain
status. Once DNS is verified, Vercel provisions HTTPS for the hostname. DNS
often updates quickly, but allow up to 24 hours.

After the hostname is valid, redeploy once so the Production environment uses
the custom-domain values. Verify DNS from PowerShell with:

```powershell
Resolve-DnsName -Type CNAME ecofem.secora.dev
```

## 5. Update website content

All content changes use the normal Git workflow:

1. Edit `ecofem/content.py` and/or a template.
2. Put new images under `static/images/`.
3. Test locally.
4. Commit and push to `main`.

```powershell
py manage.py check
py manage.py test
git add ecofem/content.py static/images
git commit -m "content: update EcoFem team profiles"
git push origin main
```

Each push to `main` triggers a new Vercel production deployment.

## 6. Verify production

Check that:

- `/`, `/about/`, `/innovation/`, `/impact/`, `/team/`, `/updates/` and
  `/contact/` load over HTTPS
- CSS, JavaScript, favicon and static images load
- any code-added team and update detail pages load
- the mobile menu works
- the Contact button opens the visitor's email application after an official
  address is added to `ecofem/content.py`
- an unknown URL displays the custom 404 page
- `/admin/` does not exist

## Troubleshooting

### `DJANGO_SECRET_KEY must be configured`

Add `DJANGO_SECRET_KEY` to the current Vercel environment and redeploy.

### `DisallowedHost`

Add the hostname to `DJANGO_ALLOWED_HOSTS` without `https://` or a path.

### A newly added image does not appear

Confirm that the image is inside `static/images/`, its path in
`ecofem/content.py` starts with `images/`, and the image was committed to Git.

### Static files fail during deployment

Do not set a custom output directory. Vercel automatically runs Django's
`collectstatic` because `STATIC_ROOT` is configured.

## Official references

- Vercel Django deployment: <https://vercel.com/docs/frameworks/full-stack/django>
- Vercel Python runtime: <https://vercel.com/docs/functions/runtimes/python>
- Django deployment checklist: <https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/>
