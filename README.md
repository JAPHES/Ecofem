# EcoFem Website

EcoFem is a responsive Django informational website for a menstrual-health and
circular-materials innovation developing biodegradable sanitary pad prototypes
with processed water hyacinth fibres.

This version is deliberately **database-free**. It has no admin area, accounts,
database, migrations, uploads, object storage, checkout or payments. Public
content is edited in `ecofem/content.py`, while all images are committed under
`static/images/`.

## Pages and features

- Home, About, Innovation, Impact, Team, Updates and Contact pages
- Optional code-managed team profiles and update detail pages
- Optional code-managed partner and gallery sections
- Static CSS, JavaScript, brand artwork and content images
- Responsive Bootstrap 5 design and accessible markup
- SEO descriptions, canonical URLs and Open Graph metadata
- Custom 404 and 500 pages
- A contact composer that opens the visitor's email app
- No server-side storage of contact details
- Automated tests that run without creating a test database

## Technology

- Python 3.12
- Django 5.2 LTS
- python-dotenv
- Bootstrap 5 and Bootstrap Icons
- Custom CSS and vanilla JavaScript

## Project structure

```text
ECOFEM/
├── manage.py
├── ecofem_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── ecofem/
│   ├── content.py        # Edit public content here
│   ├── context_processors.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── ecofem/
│   ├── includes/
│   └── errors/
├── static/
│   ├── css/main.css
│   ├── js/main.js
│   └── images/
├── .env.example
├── .python-version
├── vercel.json
├── DEPLOYMENT.md
└── requirements.txt
```

## Run on Windows

Open PowerShell in the folder that contains `manage.py`:

```powershell
cd C:\Users\User\OneDrive\Desktop\ECOFEM
py -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py runserver
```

Open <http://127.0.0.1:8000/>. There is no `migrate` or `createsuperuser`
step because this version does not use a database or Django admin.

Run checks with:

```powershell
py manage.py check
py manage.py test
```

## Edit site details

Open `ecofem/content.py` and update the `SITE` dictionary. This controls the
mission, vision, story, values, contact details and social links.

Set the real email before launch:

```python
"email": "hello@your-real-domain.org",
```

When an email is present, the Contact form builds a `mailto:` link and opens
the visitor's own email application. The website does not receive or store the
form values.

## Add a team member

1. Copy the approved profile photo to `static/images/team/`.
2. Add an entry to `TEAM_MEMBERS` in `ecofem/content.py`.
3. Restart the local development server if needed.

```python
TEAM_MEMBERS = [
    {
        "full_name": "Replace With Confirmed Name",
        "slug": "confirmed-name",
        "profile_photo": "images/team/confirmed-name.jpg",
        "role": "Confirmed EcoFem Role",
        "expertise": "Confirmed Area of Expertise",
        "short_bio": "Approved concise biography.",
        "professional_background": "Approved professional background.",
        "contribution": "What this person brings to EcoFem.",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": True,
        "is_active": True,
    },
]
```

Use a unique lowercase slug with hyphens. Set `is_founder_or_lead` to `True`
for the one confirmed founder/project lead. Up to four featured people appear
on the homepage.

## Add an update

Copy its image to `static/images/updates/`, import `date` at the top of
`content.py`, and add an entry to `UPDATES`:

```python
from datetime import date

UPDATES = [
    {
        "title": "Confirmed update title",
        "slug": "confirmed-update-title",
        "featured_image": "images/updates/confirmed-update.jpg",
        "short_description": "A concise, factual summary.",
        "content": "The approved full update text.",
        "publication_date": date(2026, 1, 15),
        "author": "EcoFem Team",
        "is_featured": False,
        "is_published": True,
    },
]
```

Keep newest entries first. Leave `UPDATES` empty until real news is approved.

## Add a partner

Copy the approved logo to `static/images/partners/`, then add:

```python
PARTNERS = [
    {
        "name": "Confirmed Organisation",
        "logo": "images/partners/organisation-logo.png",
        "partner_type": "Research",
        "website_url": "https://organisation.example/",
    },
]
```

Do not add organisations or logos until the relationship and usage permission
are confirmed.

## Add gallery images

Copy approved photographs to `static/images/gallery/`, then add:

```python
GALLERY_IMAGES = [
    {
        "image": "images/gallery/prototype-session.jpg",
        "title": "Prototype development session",
        "caption": "Approved descriptive caption.",
        "category": "Prototype",
    },
]
```

## Replace existing artwork

Current project assets are in `static/images/`. You can replace them while
keeping the same filenames, or update their template paths:

- `ecofem-hero.png`
- `water-hyacinth-process.png`
- `favicon.svg`

Commit every new static image to Git so Vercel can deploy it. Do not place
content images in a `media` directory because this version has no upload/media
storage system.

## Environment variables

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Unique secret used internally by Django |
| `DJANGO_DEBUG` | `True` locally and `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Optional comma-separated custom hostnames |
| `DJANGO_TIME_ZONE` | Defaults to `Africa/Nairobi` |
| `DJANGO_SECURE_SSL_REDIRECT` | Normally `True` on Vercel |
| `SITE_URL` | Public base URL used in canonical and social metadata |

No database or storage environment variables are used.

## Deployment

Follow [DEPLOYMENT.md](DEPLOYMENT.md). Vercel only needs the GitHub repository
and a few Django environment variables—no Postgres, SQLite, migrations, admin
account, S3 bucket or storage integration.

## Claims policy

The website describes EcoFem as under development, being tested and preparing
for certification. Do not publish medical approval, clinical proof, safety,
certification, partnership or numerical impact claims unless they are verified.
