import os

from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_context(request):
    """Expose optional admin-managed project details to every template."""
    try:
        settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError):
        settings = None

    site_url = os.getenv("SITE_URL", "").rstrip("/")
    if not site_url:
        site_url = request.build_absolute_uri("/").rstrip("/")

    return {
        "ecofem_settings": settings,
        "site_url": site_url,
        "canonical_url": f"{site_url}{request.path}",
    }
