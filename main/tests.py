import uuid
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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

    def test_public_list_detail_and_search(self):
        # List
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.atelier.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("password", response.data[0])

        # Detail
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

        # 404 on nonexistent UUID
        missing_url = reverse("api:atelier-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_url).status_code, status.HTTP_404_NOT_FOUND)

        # Search with query parameter
        res_search = self.client.get(self.list_url, {"title": "Destruct"})
        self.assertEqual(len(res_search.data), 1)
        res_empty = self.client.get(self.list_url, {"title": "Nonexistent"})
        self.assertEqual(res_empty.data, [])

    def test_visitor_cannot_write_and_db_unchanged(self):
        # Visitor POST rejected
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

        # Visitor PATCH rejected
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Edited"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "Destructon")

        # Visitor PUT rejected
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "Destructon")

        # Visitor DELETE rejected
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

    def test_regular_user_cannot_write_and_db_unchanged(self):
        self.client.force_authenticate(user=self.visitor)

        # User POST rejected
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

        # User PATCH rejected
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Edited"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "Destructon")

        # User PUT rejected
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.atelier.refresh_from_db()
        self.assertEqual(self.atelier.title, "Destructon")

        # User DELETE rejected
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

    def test_editor_can_patch_put_but_cannot_create_or_delete(self):
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

        # Editor is REJECTED on create
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

        # Editor is REJECTED on delete
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)
        self.assertTrue(Atelier.objects.filter(pk=self.atelier.id).exists())

    def test_owner_can_do_all_actions(self):
        self.client.force_authenticate(user=self.owner)

        # Owner creates
        res = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Atelier.objects.count(), 2)
        new_id = res.data["id"]

        # Owner patches
        del_url = reverse("api:atelier-detail", args=[new_id])
        res_patch = self.client.patch(del_url, {"title": "Owner Patched"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)

        # Owner deletes
        res_del = self.client.delete(del_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Atelier.objects.count(), 1)
        self.assertFalse(Atelier.objects.filter(pk=new_id).exists())

    def test_input_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, expected_field in [
            ({"title": "   "}, "title"),
            ({"title": "<b>  </b>"}, "title"),
            ({"project_url": "invalid-url"}, "project_url"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
            ({"image_url": "not-a-url"}, "image_url"),
        ]:
            res = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(expected_field, res.data)
            self.assertEqual(Atelier.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        # Visitor cannot star
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.atelier.starred_by.count(), 0)

        # Logged in visitor can star
        self.client.force_authenticate(user=self.visitor)
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["is_starred"])
        self.assertEqual(res.data["star_count"], 1)
        self.assertEqual(self.atelier.starred_by.count(), 1)

        # Second POST toggles off
        res2 = self.client.post(self.star_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertFalse(res2.data["is_starred"])
        self.assertEqual(res2.data["star_count"], 0)
        self.assertEqual(self.atelier.starred_by.count(), 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["star_count"], 0)
        self.assertFalse(res.data["is_starred"])

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner_atelier", password="test-password"))
        res = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Atelier.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner_atelier", password="test-password"))
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        res = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Atelier.objects.filter(pk=res.data["id"]).exists())


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_exp", password="test-password", email="owner_exp@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor_exp", password="test-password")
        self.editor = User.objects.create_user(username="editor_exp", password="test-password")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.experience = Experience.objects.create(
            title="Software Engineering Intern",
            description="Developing web apps with Django",
            category="internship",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.payload = {
            "title": "Teaching Assistant",
            "description": "Mentoring students in CS",
            "category": "part-time",
            "thumbnail": "https://example.com/ta.png",
        }

    def test_public_list_detail_and_search(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], str(self.experience.id))
        self.assertEqual(res.data[0]["category_display"], "Internship")

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)

        # 404
        missing_url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_url).status_code, status.HTTP_404_NOT_FOUND)

        # Search
        res_search = self.client.get(self.list_url, {"title": "Software"})
        self.assertEqual(len(res_search.data), 1)
        res_empty = self.client.get(self.list_url, {"title": "Nonexistent"})
        self.assertEqual(res_empty.data, [])

    def test_visitor_and_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Experience.objects.count(), 1)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, "Software Engineering Intern")

    def test_editor_can_patch_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        # PATCH
        res_patch = self.client.patch(self.detail_url, {"title": "Senior Intern"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior Intern")

        # PUT
        res_put = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")

        # Rejection on POST and DELETE
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_do_all_actions(self):
        self.client.force_authenticate(user=self.owner)
        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)
        new_id = res_post.data["id"]

        del_url = reverse("api:experience-detail", args=[new_id])
        res_del = self.client.delete(del_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Experience.objects.count(), 1)

    def test_input_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes in [{"title": "   "}, {"title": "<b>  </b>"}]:
            res = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Experience.objects.count(), 1)


class SkillsAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_skill", password="test-password", email="owner_skill@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor_skill", password="test-password")
        self.editor = User.objects.create_user(username="editor_skill", password="test-password")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.skill = Skills.objects.create(
            title="Python Programming",
            description="Django, DRF, scripting",
            type="programming",
        )
        self.list_url = reverse("api:skills-list")
        self.detail_url = reverse("api:skills-detail", args=[self.skill.id])
        self.payload = {
            "title": "Digital Art",
            "description": "Concept art and illustrations",
            "type": "art",
            "thumbnail": "https://example.com/art.png",
        }

    def test_public_list_detail_and_search(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], str(self.skill.id))
        self.assertEqual(res.data[0]["type_display"], "Programming")

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)

        # 404
        missing_url = reverse("api:skills-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_url).status_code, status.HTTP_404_NOT_FOUND)

        # Search
        res_search = self.client.get(self.list_url, {"title": "Python"})
        self.assertEqual(len(res_search.data), 1)
        res_empty = self.client.get(self.list_url, {"title": "Nonexistent"})
        self.assertEqual(res_empty.data, [])

    def test_visitor_and_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Skills.objects.count(), 1)
            self.skill.refresh_from_db()
            self.assertEqual(self.skill.title, "Python Programming")

    def test_editor_can_patch_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        # PATCH
        res_patch = self.client.patch(self.detail_url, {"title": "Advanced Python"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Advanced Python")

        # PUT
        res_put = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Digital Art")

        # Rejection on POST and DELETE
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skills.objects.count(), 1)

    def test_owner_can_do_all_actions(self):
        self.client.force_authenticate(user=self.owner)
        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skills.objects.count(), 2)
        new_id = res_post.data["id"]

        del_url = reverse("api:skills-detail", args=[new_id])
        res_del = self.client.delete(del_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skills.objects.count(), 1)

    def test_input_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes in [{"title": "   "}, {"title": "<b>  </b>"}]:
            res = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Skills.objects.count(), 1)

