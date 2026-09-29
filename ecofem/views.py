from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from .content import GALLERY_IMAGES, PARTNERS, TEAM_MEMBERS, UPDATES


def _active_team():
    return [member for member in TEAM_MEMBERS if member.get("is_active", True)]


def _published_updates():
    return [update for update in UPDATES if update.get("is_published", True)]


def home(request):
    team = _active_team()
    updates = _published_updates()
    context = {
        "featured_members": [
            member for member in team if member.get("is_featured", False)
        ][:4],
        "latest_updates": updates[:3],
        "partners": PARTNERS[:8],
    }
    return render(request, "ecofem/home.html", context)


def about(request):
    founder = next(
        (
            member
            for member in _active_team()
            if member.get("is_founder_or_lead", False)
        ),
        None,
    )
    context = {
        "founder": founder,
        "partners": PARTNERS,
        "gallery_images": GALLERY_IMAGES[:6],
    }
    return render(request, "ecofem/about.html", context)


def innovation(request):
    return render(request, "ecofem/innovation.html")


def impact(request):
    return render(request, "ecofem/impact.html", {"partners": PARTNERS[:8]})


def team_list(request):
    return render(request, "ecofem/team_list.html", {"members": _active_team()})


def update_list(request):
    page_obj = Paginator(_published_updates(), 6).get_page(request.GET.get("page"))
    return render(
        request,
        "ecofem/update_list.html",
        {"page_obj": page_obj, "gallery_images": GALLERY_IMAGES[:6]},
    )


def update_detail(request, slug):
    updates = _published_updates()
    update = next((item for item in updates if item.get("slug") == slug), None)
    if update is None:
        raise Http404("Update not found")
    related_updates = [item for item in updates if item is not update][:3]
    return render(
        request,
        "ecofem/update_detail.html",
        {"update": update, "related_updates": related_updates},
    )


def contact(request):
    return render(request, "ecofem/contact.html")


def custom_404(request, exception=None):
    response = render(request, "errors/404.html", status=404)
    response["Cache-Control"] = "no-store"
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response


def custom_500(request):
    return render(request, "errors/500.html", status=500)
