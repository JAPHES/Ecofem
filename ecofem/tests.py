from datetime import date
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from django.utils.html import escape

from .content import TEAM_MEMBERS


SAMPLE_MEMBER = {
    "full_name": "Example Member",
    "slug": "example-member",
    "profile_photo": "images/team/example-member.jpg",
    "role": "Project Role",
    "expertise": "Project Expertise",
    "short_bio": "Confirmed profile information.",
    "professional_background": "Confirmed professional background.",
    "contribution": "Confirmed project contribution.",
    "leadership_story": "",
    "vision_for_ecofem": "",
    "email": "",
    "linkedin_url": "",
    "is_founder_or_lead": False,
    "is_featured": True,
    "is_active": True,
}

SAMPLE_UPDATE = {
    "title": "Prototype learning update",
    "slug": "prototype-learning-update",
    "featured_image": "images/updates/prototype-learning.jpg",
    "short_description": "A factual project development summary.",
    "content": "Confirmed information about current development work.",
    "publication_date": date(2026, 1, 15),
    "author": "EcoFem Team",
    "is_featured": False,
    "is_published": True,
}


class PublicPageTests(SimpleTestCase):
    def test_main_pages_render_without_database(self):
        for name in (
            "home",
            "about",
            "innovation",
            "impact",
            "team_list",
            "update_list",
            "contact",
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(f"ecofem:{name}"))
                self.assertEqual(response.status_code, 200)

    def test_project_uses_only_djangos_inert_dummy_backend(self):
        self.assertEqual(
            settings.DATABASES["default"]["ENGINE"],
            "django.db.backends.dummy",
        )
        self.assertNotIn("django.contrib.admin", settings.INSTALLED_APPS)

    def test_admin_route_does_not_exist(self):
        self.assertEqual(self.client.get("/admin/").status_code, 404)

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

    @override_settings(SITE_URL="https://ecofem.secora.dev")
    def test_custom_domain_is_used_for_canonical_metadata(self):
        response = self.client.get(reverse("ecofem:about"))
        self.assertEqual(
            response.context["canonical_url"],
            "https://ecofem.secora.dev/about/",
        )


class CodeManagedContentTests(SimpleTestCase):
    def test_confirmed_team_members_render_with_photo_placeholders(self):
        self.assertEqual(len(TEAM_MEMBERS), 10)
        response = self.client.get(reverse("ecofem:team_list"))

        for member in TEAM_MEMBERS:
            with self.subTest(member=member["full_name"]):
                self.assertEqual(member["profile_photo"], "")
                self.assertContains(response, member["full_name"])
                self.assertContains(response, member["role"])
                self.assertContains(response, escape(member["expertise"]))

        self.assertContains(response, "Profile photo placeholder for", count=10)

    def test_project_lead_profile_includes_supplied_experience(self):
        response = self.client.get(
            reverse("ecofem:team_detail", args=["yvonne-achieng"])
        )
        self.assertContains(response, "Yvonne Achieng’")
        self.assertContains(response, "applied statistician")

    @patch("ecofem.views.TEAM_MEMBERS", [SAMPLE_MEMBER])
    def test_team_profile_uses_code_content_and_static_image(self):
        response = self.client.get(
            reverse("ecofem:team_detail", args=[SAMPLE_MEMBER["slug"]])
        )
        self.assertContains(response, SAMPLE_MEMBER["full_name"])
        self.assertContains(response, "/static/images/team/example-member.jpg")

    def test_unknown_team_profile_is_404(self):
        response = self.client.get(reverse("ecofem:team_detail", args=["missing"]))
        self.assertEqual(response.status_code, 404)

    @patch("ecofem.views.UPDATES", [SAMPLE_UPDATE])
    def test_update_uses_code_content_and_static_image(self):
        response = self.client.get(
            reverse("ecofem:update_detail", args=[SAMPLE_UPDATE["slug"]])
        )
        self.assertContains(response, SAMPLE_UPDATE["title"])
        self.assertContains(response, "/static/images/updates/prototype-learning.jpg")

    def test_contact_page_explains_that_details_are_not_stored(self):
        response = self.client.get(reverse("ecofem:contact"))
        self.assertContains(response, "does not submit or store", status_code=200)
