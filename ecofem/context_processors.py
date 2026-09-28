from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_context(request):
    """Expose optional admin-managed project details to every template."""
    try:
        settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError):
        settings = None
    return {"ecofem_settings": settings}
