from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Experience, Skills, Atelier


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

        self.skills = Skills.objects.create(
            title="The Arts",
            description="Concept Art, Writing, Character Design, 3D Character and Environment Modelling.",
            type="art",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_skill_model(self):
        self.assertEqual(str(self.skills), "The Arts")
        self.assertEqual(self.skills.type, "art")

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience found.")
    
    def test_empty_skill_page(self):
        Skills.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, "No skills have been added.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class AtelierAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_atelier", password="test-password", email="owner_atelier@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor_atelier", password="test-password")
        self.editor = User.objects.create_user(username="editor_atelier", password="test-password")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.atelier = Atelier.objects.create(
            title="Destructon",
            project_url="https://example.com/destructon",
            image_url="https://example.com/destructon.png",
        )
        self.list_url = reverse("api:atelier-list")
        self.detail_url = reverse("api:atelier-detail", args=[self.atelier.id])
        self.star_url = reverse("api:atelier-star", args=[self.atelier.id])
        self.payload = {
            "title": "New Atelier Item",
            "project_url": "https://example.com/new",
            "image_url": "https://example.com/new.png",
        }

    def test_visitor_can_read_only(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.atelier.id))
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Edited"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_can_star_but_not_edit(self):
        self.client.force_authenticate(user=self.visitor)
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["is_starred"])
        self.assertEqual(res.data["star_count"], 1)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Edited"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_patch_put_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        # Editor can PATCH
        response = self.client.patch(self.detail_url, {"title": "Patched by Editor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "Patched by Editor")

        # Editor can PUT
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "New Atelier Item")

        # Editor is REJECTED on create and delete
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_do_all_actions(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        new_id = res.data["id"]

        del_url = reverse("api:atelier-detail", args=[new_id])
        res = self.client.delete(del_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
