from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ContactForm
from .models import GalleryImage, Partner, SiteSettings, TeamMember, Update


def home(request):
    today = timezone.localdate()
    active_team = TeamMember.objects.filter(is_active=True)
    partners = Partner.objects.filter(active=True)
    updates = Update.objects.filter(is_published=True, publication_date__lte=today)
    project_settings = SiteSettings.objects.first()
    active_team_count = active_team.count()
    active_partner_count = partners.count()
    context = {
        "featured_members": active_team.filter(is_featured=True)[:4],
        "latest_updates": updates[:3],
        "partners": partners[:8],
        "active_team_count": active_team_count,
        "active_partner_count": active_partner_count,
        "published_update_count": updates.count(),
        "project_settings": project_settings,
        "show_statistics": (
            active_team_count > 0
            or active_partner_count > 0
            or (
                project_settings
                and (
                    project_settings.prototypes_developed is not None
                    or project_settings.tests_conducted is not None
                )
            )
        ),
    }
    return render(request, "ecofem/home.html", context)


def about(request):
    context = {
        "project_settings": SiteSettings.objects.first(),
        "project_lead": TeamMember.objects.filter(
            is_active=True, is_founder_or_lead=True
        ).first(),
        "partners": Partner.objects.filter(active=True),
        "gallery_images": GalleryImage.objects.filter(active=True)[:6],
    }
    return render(request, "ecofem/about.html", context)


def innovation(request):
    return render(request, "ecofem/innovation.html")


def impact(request):
    return render(
        request,
        "ecofem/impact.html",
        {"partners": Partner.objects.filter(active=True)[:8]},
    )


def team_list(request):
    members = TeamMember.objects.filter(is_active=True)
    return render(request, "ecofem/team_list.html", {"members": members})


def team_detail(request, slug):
    member = get_object_or_404(TeamMember, slug=slug, is_active=True)
    return render(request, "ecofem/team_detail.html", {"member": member})


def update_list(request):
    updates = Update.objects.filter(
        is_published=True,
        publication_date__lte=timezone.localdate(),
    )
    page_obj = Paginator(updates, 6).get_page(request.GET.get("page"))
    gallery_images = GalleryImage.objects.filter(active=True)[:6]
    return render(
        request,
        "ecofem/update_list.html",
        {"page_obj": page_obj, "gallery_images": gallery_images},
    )


def update_detail(request, slug):
    update = get_object_or_404(
        Update,
        slug=slug,
        is_published=True,
        publication_date__lte=timezone.localdate(),
    )
    related_updates = (
        Update.objects.filter(
            is_published=True,
            publication_date__lte=timezone.localdate(),
        )
        .exclude(pk=update.pk)[:3]
    )
    return render(
        request,
        "ecofem/update_detail.html",
        {"update": update, "related_updates": related_updates},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for reaching out. Your message has been received, "
                "and the EcoFem team will respond as soon as possible.",
            )
            return redirect("ecofem:contact")
    else:
        form = ContactForm()
    return render(request, "ecofem/contact.html", {"form": form})


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500(request):
    return render(request, "errors/500.html", status=500)
