from datetime import timedelta
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import ContactMessage, GalleryImage, Partner, TeamMember, Update


class PublicPageTests(TestCase):
    def test_main_pages_render(self):
        names = (
            "home",
            "about",
            "innovation",
            "impact",
            "team_list",
            "update_list",
            "contact",
        )
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(reverse(f"ecofem:{name}"))
                self.assertEqual(response.status_code, 200)

    def test_unknown_page_returns_custom_404(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "This page has drifted away", status_code=404)

    def test_canonical_and_open_graph_urls_are_absolute(self):
        response = self.client.get(reverse("ecofem:about"))
        self.assertEqual(response.context["canonical_url"], "http://testserver/about/")
        self.assertContains(
            response,
            '<meta property="og:image" content="http://testserver/static/images/',
            html=False,
        )


class TeamTests(TestCase):
    def test_active_team_member_profile_is_public(self):
        member = TeamMember.objects.create(
            full_name="Sample Profile — Replace in Admin",
            role="Project Role",
            expertise="Area of Expertise",
            short_bio="Placeholder content for a confirmed team member.",
        )
        response = self.client.get(member.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, member.full_name)

    def test_inactive_team_member_profile_is_hidden(self):
        member = TeamMember.objects.create(
            full_name="Inactive Profile",
            role="Project Role",
            expertise="Expertise",
            short_bio="Not currently public.",
            is_active=False,
        )
        self.assertEqual(self.client.get(member.get_absolute_url()).status_code, 404)

    def test_duplicate_names_receive_unique_slugs(self):
        first = TeamMember.objects.create(
            full_name="Sample Member",
            role="Role",
            expertise="Expertise",
            short_bio="Biography content.",
        )
        second = TeamMember.objects.create(
            full_name="Sample Member",
            role="Role",
            expertise="Expertise",
            short_bio="Biography content.",
        )
        self.assertEqual(first.slug, "sample-member")
        self.assertEqual(second.slug, "sample-member-2")


class UpdateTests(TestCase):
    def create_update(self, **overrides):
        data = {
            "title": "Prototype learning update",
            "short_description": "A factual project development summary.",
            "content": "Confirmed information about current development work.",
            "publication_date": timezone.localdate(),
            "is_published": True,
        }
        data.update(overrides)
        return Update.objects.create(**data)

    def test_published_update_is_visible(self):
        update = self.create_update()
        response = self.client.get(update.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, update.title)

    def test_draft_and_future_updates_are_hidden(self):
        draft = self.create_update(title="Draft", is_published=False)
        future = self.create_update(
            title="Future",
            publication_date=timezone.localdate() + timedelta(days=1),
        )
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(future.get_absolute_url()).status_code, 404)

    def test_home_shows_only_three_latest_updates(self):
        for index in range(4):
            self.create_update(
                title=f"Update {index}",
                publication_date=timezone.localdate() - timedelta(days=index),
            )
        response = self.client.get(reverse("ecofem:home"))
        self.assertEqual(len(response.context["latest_updates"]), 3)


class ContactTests(TestCase):
    def test_valid_contact_form_stores_message(self):
        response = self.client.post(
            reverse("ecofem:contact"),
            {
                "name": "Interested Collaborator",
                "email": "collaborator@example.com",
                "organisation": "Example Organisation",
                "subject": "Research collaboration",
                "message": "We would like to discuss a responsible research collaboration.",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("ecofem:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        stored_messages = get_messages(response.wsgi_request)
        self.assertTrue(any("received" in str(message) for message in stored_messages))

    def test_short_contact_message_is_rejected(self):
        response = self.client.post(
            reverse("ecofem:contact"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "subject": "Question",
                "message": "Too short",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "at least 20 characters")
        self.assertFalse(ContactMessage.objects.exists())


class AdminRegistrationTests(TestCase):
    def test_content_models_are_registered(self):
        for model in (TeamMember, Partner, Update, GalleryImage, ContactMessage):
            with self.subTest(model=model):
                self.assertIn(model, site._registry)


class AdminWorkflowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.media_directory = tempfile.mkdtemp(prefix="ecofem-test-media-")
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory)
        cls.media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.media_override.disable()
        shutil.rmtree(cls.media_directory, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="site-admin",
            email="admin@example.com",
            password="temporary-test-password",
        )
        self.client.force_login(self.admin)

    def test_admin_content_lists_are_accessible(self):
        names = (
            "teammember",
            "partner",
            "update",
            "galleryimage",
            "contactmessage",
        )
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(reverse(f"admin:ecofem_{name}_changelist"))
                self.assertEqual(response.status_code, 200)

    def test_admin_can_create_edit_and_delete_team_member(self):
        response = self.client.post(
            reverse("admin:ecofem_teammember_add"),
            {
                "full_name": "Admin Managed Member",
                "slug": "admin-managed-member",
                "role": "Project Role",
                "expertise": "Project Expertise",
                "short_bio": "A concise and confirmed professional biography.",
                "professional_background": "Confirmed professional background.",
                "contribution": "A confirmed contribution to the project.",
                "leadership_story": "",
                "vision_for_ecofem": "",
                "email": "",
                "linkedin_url": "",
                "display_order": 1,
                "is_featured": "on",
                "is_active": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302)
        member = TeamMember.objects.get(slug="admin-managed-member")

        response = self.client.post(
            reverse("admin:ecofem_teammember_change", args=[member.pk]),
            {
                "full_name": member.full_name,
                "slug": member.slug,
                "role": "Updated Project Role",
                "expertise": member.expertise,
                "short_bio": member.short_bio,
                "professional_background": member.professional_background,
                "contribution": member.contribution,
                "leadership_story": "",
                "vision_for_ecofem": "",
                "email": "",
                "linkedin_url": "",
                "display_order": 1,
                "is_featured": "on",
                "is_active": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302)
        member.refresh_from_db()
        self.assertEqual(member.role, "Updated Project Role")

        response = self.client.post(
            reverse("admin:ecofem_teammember_delete", args=[member.pk]),
            {"post": "yes"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TeamMember.objects.filter(pk=member.pk).exists())

    def test_admin_can_add_partner_update_and_gallery_image(self):
        partner_response = self.client.post(
            reverse("admin:ecofem_partner_add"),
            {
                "name": "Confirmed Test Partner",
                "description": "Test-only partner content.",
                "website_url": "https://example.com/",
                "partner_type": "research",
                "display_order": 0,
                "active": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(partner_response.status_code, 302)
        self.assertTrue(Partner.objects.filter(name="Confirmed Test Partner").exists())

        update_response = self.client.post(
            reverse("admin:ecofem_update_add"),
            {
                "title": "Confirmed test update",
                "slug": "confirmed-test-update",
                "short_description": "A test description used only by the automated suite.",
                "content": "A test update used to verify Django admin publishing.",
                "publication_date": timezone.localdate().isoformat(),
                "author": "EcoFem Team",
                "is_published": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(update_response.status_code, 302)
        self.assertTrue(Update.objects.filter(slug="confirmed-test-update").exists())

        one_pixel_gif = SimpleUploadedFile(
            "project-image.gif",
            (
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff"
                b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
                b"\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        gallery_response = self.client.post(
            reverse("admin:ecofem_galleryimage_add"),
            {
                "image": one_pixel_gif,
                "title": "Confirmed test gallery image",
                "caption": "Test-only gallery caption.",
                "category": "prototype",
                "display_order": 0,
                "active": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(gallery_response.status_code, 302)
        gallery_image = GalleryImage.objects.get(title="Confirmed test gallery image")
        self.assertTrue(gallery_image.image.storage.exists(gallery_image.image.name))

    def test_uploaded_team_photo_url_renders_on_public_profile(self):
        one_pixel_gif = SimpleUploadedFile(
            "profile.gif",
            (
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff"
                b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
                b"\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        member = TeamMember.objects.create(
            full_name="Member With Photo",
            role="Project Role",
            expertise="Project Expertise",
            short_bio="A confirmed profile for the image rendering test.",
            profile_photo=one_pixel_gif,
        )
        response = self.client.get(member.get_absolute_url())
        self.assertContains(response, member.profile_photo.url)
        self.assertTrue(member.profile_photo.storage.exists(member.profile_photo.name))
