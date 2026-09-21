from django.urls import path

from main.views import (create_atelier, create_experience, delete_atelier, delete_experience, get_atelier_json, get_experience_json, show_main, show_experience, show_atelier, show_skills, create_skills, get_skills_json, delete_skills)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("atelier/", show_atelier, name="show_atelier"),
    path("atelier/add/", create_atelier, name="create_atelier"),
    path("api/atelier/", get_atelier_json, name="get_atelier_json"),
    path("atelier/<uuid:atelier_id>/delete/", delete_atelier, name="delete_atelier"),
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skills, name="create_skills"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/<uuid:skills_id>/delete/", delete_skills, name="delete_skills"),
]