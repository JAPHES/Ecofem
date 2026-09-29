import os

from .content import SITE


def site_context(request):
    """Expose code-managed site details and absolute metadata URLs."""
    site_url = os.getenv("SITE_URL", "").rstrip("/")
    if not site_url:
        site_url = request.build_absolute_uri("/").rstrip("/")

    return {
        "site": SITE,
        "site_url": site_url,
        "canonical_url": f"{site_url}{request.path}",
    }
