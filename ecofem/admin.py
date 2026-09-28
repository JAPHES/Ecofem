from django.contrib import admin

from .models import (
    ContactMessage,
    GalleryImage,
    Partner,
    SiteSettings,
    TeamMember,
    Update,
)


admin.site.site_header = "EcoFem Administration"
admin.site.site_title = "EcoFem Admin"
admin.site.index_title = "Website content management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Project", {"fields": ("site_name", "short_description", "project_story")}),
        ("Purpose", {"fields": ("mission", "vision", "values")}),
        (
            "Contact and social",
            {
                "fields": (
                    "email",
                    "phone",
                    "location",
                    "linkedin_url",
                    "instagram_url",
                    "facebook_url",
                )
            },
        ),
        (
            "Verified progress figures",
            {
                "fields": ("prototypes_developed", "tests_conducted"),
                "description": "Leave figures blank until they can be verified.",
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "role",
        "expertise",
        "is_founder_or_lead",
        "is_featured",
        "is_active",
    )
    search_fields = ("full_name", "role", "expertise", "short_bio")
    list_filter = ("is_founder_or_lead", "is_featured", "is_active")
    ordering = ("display_order", "full_name")
    prepopulated_fields = {"slug": ("full_name",)}
    list_editable = ("is_featured", "is_active")
    fieldsets = (
        ("Profile", {"fields": ("full_name", "slug", "profile_photo", "role", "expertise")}),
        (
            "Biography",
            {"fields": ("short_bio", "professional_background", "contribution")},
        ),
        (
            "Leadership",
            {
                "fields": ("is_founder_or_lead", "leadership_story", "vision_for_ecofem"),
                "classes": ("collapse",),
            },
        ),
        ("Contact", {"fields": ("email", "linkedin_url")}),
        ("Display", {"fields": ("display_order", "is_featured", "is_active")}),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "display_order", "active")
    search_fields = ("name", "description")
    list_filter = ("partner_type", "active")
    ordering = ("display_order", "name")
    list_editable = ("display_order", "active")


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "publication_date",
        "author",
        "is_featured",
        "is_published",
    )
    search_fields = ("title", "short_description", "content", "author")
    list_filter = ("is_featured", "is_published", "publication_date")
    ordering = ("-publication_date",)
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "is_published")
    date_hierarchy = "publication_date"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "display_order", "active")
    search_fields = ("title", "caption")
    list_filter = ("category", "active")
    ordering = ("display_order", "title")
    list_editable = ("display_order", "active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "organisation", "subject", "created_at", "is_read")
    search_fields = ("name", "email", "organisation", "subject", "message")
    list_filter = ("is_read", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("name", "email", "organisation", "subject", "message", "created_at")
    fields = ("name", "email", "organisation", "subject", "message", "created_at", "is_read")

    def has_add_permission(self, request):
        return False
