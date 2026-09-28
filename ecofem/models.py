from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def unique_slug(instance, value, slug_field="slug"):
    """Return a stable, unique slug for a model instance."""
    base_slug = slugify(value) or "item"
    candidate = base_slug
    queryset = instance.__class__.objects.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    counter = 2
    while queryset.filter(**{slug_field: candidate}).exists():
        candidate = f"{base_slug}-{counter}"
        counter += 1
    return candidate


class SiteSettings(models.Model):
    """Admin-editable project details used across the public site."""

    site_name = models.CharField(max_length=80, default="EcoFem")
    short_description = models.TextField(
        default=(
            "Developing affordable, biodegradable sanitary pads using processed "
            "water hyacinth fibres."
        )
    )
    project_story = models.TextField(blank=True)
    mission = models.TextField(
        default=(
            "To develop accessible, sustainable and high-performing menstrual "
            "hygiene solutions while transforming environmental waste into useful resources."
        )
    )
    vision = models.TextField(
        default=(
            "A future where every woman and girl can access safe and affordable "
            "menstrual products without compromising the environment."
        )
    )
    values = models.TextField(
        default="Innovation\nSustainability\nDignity\nInclusivity\nQuality\nCommunity Impact",
        help_text="Enter one value per line.",
    )
    email = models.EmailField(blank=True, default="hello@example.com")
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=180, blank=True, default="Location to be confirmed")
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    prototypes_developed = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank until a verified figure is available.",
    )
    tests_conducted = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank until a verified figure is available.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None

    @property
    def value_list(self):
        return [value.strip() for value in self.values.splitlines() if value.strip()]


class TeamMember(models.Model):
    full_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    profile_photo = models.ImageField(upload_to="team/", blank=True)
    role = models.CharField(max_length=120)
    expertise = models.CharField(max_length=180)
    short_bio = models.TextField(help_text="A concise biography for the profile page.")
    professional_background = models.TextField(blank=True)
    contribution = models.TextField(
        blank=True,
        help_text="What this person brings to EcoFem.",
    )
    leadership_story = models.TextField(
        blank=True,
        help_text="Optional founder/project leadership story.",
    )
    vision_for_ecofem = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_founder_or_lead = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "full_name")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.full_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ecofem:team_detail", kwargs={"slug": self.slug})


class Partner(models.Model):
    class PartnerType(models.TextChoices):
        ACADEMIC = "academic", "Academic"
        RESEARCH = "research", "Research"
        GOVERNMENT = "government", "Government"
        NGO = "ngo", "NGO"
        INNOVATION = "innovation", "Innovation Support"
        MANUFACTURING = "manufacturing", "Manufacturing"
        COMMUNITY = "community", "Community"

    name = models.CharField(max_length=160)
    logo = models.ImageField(upload_to="partners/", blank=True)
    description = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    partner_type = models.CharField(
        max_length=30,
        choices=PartnerType.choices,
        default=PartnerType.INNOVATION,
    )
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name


class Update(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    featured_image = models.ImageField(upload_to="updates/", blank=True)
    short_description = models.CharField(max_length=320)
    content = models.TextField()
    publication_date = models.DateField()
    author = models.CharField(max_length=120, blank=True, default="EcoFem Team")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-publication_date", "-created_at")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ecofem:update_detail", kwargs={"slug": self.slug})


class GalleryImage(models.Model):
    class Category(models.TextChoices):
        TEAM = "team", "Team"
        LABORATORY = "laboratory", "Laboratory"
        PROTOTYPE = "prototype", "Prototype"
        EVENTS = "events", "Events"
        WATER_HYACINTH = "water_hyacinth", "Water Hyacinth"
        COMMUNITY = "community", "Community"

    image = models.ImageField(upload_to="gallery/")
    title = models.CharField(max_length=160)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=Category.choices)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name_plural = "gallery images"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    organisation = models.CharField(max_length=180, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.subject} — {self.name}"
