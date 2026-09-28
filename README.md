# EcoFem Website

EcoFem is a Django-powered informational website for a menstrual-health and circular-materials innovation developing biodegradable sanitary pad prototypes with processed water hyacinth fibres.

This first MVP is designed to build awareness and trust, explain the innovation responsibly, introduce the project team, document progress, showcase confirmed partners, publish updates and receive enquiries. It is **not** an e-commerce platform and contains no public accounts, ordering, payments, inventory or team-member login system.

## Features

- Responsive Home, About, Innovation, Impact, Team, Updates and Contact pages
- Database-managed team profiles with featured and project-lead controls
- Dedicated, slug-based team member profile pages
- Database-managed partners and supporters
- Publishable, slug-based project updates with draft and future-post protection
- Categorised project gallery
- Contact form with CSRF protection, validation, success feedback and database storage
- Admin-editable mission, vision, values, project story, contact details and verified statistics
- Customised Django admin lists, filters, search, ordering and content fieldsets
- Responsive Bootstrap 5 interface with an EcoFem-specific design system
- Semantic page titles, descriptions, Open Graph metadata and accessible image labels
- Custom 404 and 500 pages
- Automated tests for all public routes, protected content states, contact submissions, slugs and admin registration
- Careful product language that distinguishes prototypes, testing and certification preparation

## Technology stack

- Python 3.10+
- Django 5.2 LTS
- SQLite for local development
- Pillow for image uploads
- python-dotenv for environment configuration
- Bootstrap 5, Bootstrap Icons and custom CSS
- Vanilla JavaScript for subtle reveal effects, navbar state and mobile navigation

## Project structure

```text
ECOFEM/
├── manage.py
├── ecofem_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── ecofem/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── ecofem/
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── innovation.html
│   │   ├── impact.html
│   │   ├── team_list.html
│   │   ├── team_detail.html
│   │   ├── update_list.html
│   │   ├── update_detail.html
│   │   └── contact.html
│   ├── includes/
│   │   ├── page_header.html
│   │   ├── team_card.html
│   │   ├── update_card.html
│   │   ├── partner_grid.html
│   │   ├── gallery.html
│   │   └── get_involved.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/main.css
│   ├── js/main.js
│   └── images/
│       ├── ecofem-hero.png
│       ├── water-hyacinth-process.png
│       └── favicon.svg
├── media/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows setup

Open PowerShell in the project folder.

### 1. Create and activate a virtual environment

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
py -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create the local environment file

```powershell
Copy-Item .env.example .env
```

Generate a strong development/production secret with:

```powershell
py -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
```

Paste that value into `DJANGO_SECRET_KEY` in `.env`.

### 4. Apply database migrations

```powershell
py manage.py migrate
```

When models change later, use:

```powershell
py manage.py makemigrations
py manage.py migrate
```

### 5. Create the admin account

```powershell
py manage.py createsuperuser
```

Enter the requested username, email and password. This Django superuser is the only account type required for the MVP.

### 6. Run the development server

```powershell
py manage.py runserver
```

Visit:

- Website: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Environment variables

| Variable | Purpose | Development example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Cryptographic signing secret | Generate a unique random value |
| `DJANGO_DEBUG` | Enables development diagnostics | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames | `127.0.0.1,localhost` |
| `DJANGO_TIME_ZONE` | Project time zone | `Africa/Nairobi` |
| `DJANGO_SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `False` locally; normally `True` in production |

Never commit `.env`. For production, set `DJANGO_DEBUG=False`, use a unique secret, list the real domain in `DJANGO_ALLOWED_HOSTS`, serve over HTTPS and configure a production web server to serve collected static files and uploaded media.

## Managing website content

Sign in at `/admin/` using the superuser account.

### Site settings

Open **Site settings** and create the single project settings record. This controls:

- short project description
- project story
- mission, vision and values
- public email, phone, location and social links
- optional verified counts for prototypes and tests

Enter one project value per line. Leave prototype and test figures blank until confirmed; blank figures are not shown publicly.

### Adding EcoFem team members

1. Open **Team members** and select **Add team member**.
2. Enter the confirmed name, role and expertise.
3. Upload a professional portrait.
4. Add a concise biography, professional background and contribution.
5. For the founder or project lead, enable **Is founder or lead** and add the leadership story and EcoFem vision.
6. Enable **Is featured** to show the person on the homepage. The homepage displays up to four featured people.
7. Set **Display order**; lower numbers appear first.
8. Keep **Is active** enabled when the profile is ready to publish.

Team members do not receive accounts and never need to sign in. They are public website content managed by the Django administrator.

### Adding confirmed partners

1. Open **Partners** and select **Add partner**.
2. Enter the confirmed organisation name, type and description.
3. Upload its approved logo and add its official website if available.
4. Set the display order and keep **Active** enabled to show it publicly.

Do not add an organisation until the relationship and logo usage are confirmed.

### Publishing updates

1. Open **Updates** and select **Add update**.
2. Add the title, image, short card description, full content, date and author.
3. Optionally mark the post as featured.
4. Enable **Is published** only when the content is approved.

Drafts and posts with future publication dates are not visible on the public site. The three latest eligible posts appear automatically on the homepage.

### Adding gallery images

Open **Gallery images**, upload an approved image, add useful alt-friendly title and caption text, choose its category, and set its display order. Only active images appear publicly.

### Reviewing contact messages

Open **Contact messages** to search and review enquiries. Visitor-submitted details are read-only except for the **Is read** tracking flag. There is no visitor account and no automatic email sending in this MVP.

## Static and media files

- Source static assets live in `static/`.
- Admin-uploaded content is stored in `media/`.
- Django serves media automatically only when local `DEBUG=True`.
- Uploaded files are intentionally ignored by Git except for `media/.gitkeep`.

For a deployment build:

```powershell
py manage.py collectstatic --noinput
```

Configure the production platform or web server to serve `STATIC_ROOT` and `MEDIA_ROOT`. Back up the media folder and database because both contain managed project content.

## Tests and checks

Run the automated suite:

```powershell
py manage.py test
```

Run Django's deployment-oriented checks before launch:

```powershell
py manage.py check
py manage.py check --deploy
```

The normal `--deploy` warnings about HTTPS and cookie security should be addressed in the actual hosting environment, not by weakening local development settings.

## Content and image placeholders to replace

Before public launch, review or replace:

- the generated concept hero and water-hyacinth process images with approved EcoFem photography, if available
- the favicon/logo placeholder with the final EcoFem brand assets
- placeholder email and location in Site settings
- all social media URLs
- the project story and official leadership profile
- confirmed team biographies and profile photos
- confirmed partner names, descriptions, websites and approved logos
- real project updates and gallery photographs
- verified prototype/test counts, or leave them blank
- any hosting-specific Open Graph absolute image URL and domain configuration

No sample people, organisations, certifications, regulatory approvals, test figures or news posts are inserted into the production database.

## Product-claim policy

Public copy deliberately uses language such as “under development,” “prototype,” “being tested,” “aims to” and “preparing for certification.” Do not change this to “medically approved,” “clinically proven,” “certified,” “completely safe” or similar language unless the claim is verified and documented.
