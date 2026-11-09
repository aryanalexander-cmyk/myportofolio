from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),

    # Assignment model endpoints
    path("atelier/", api_views.atelier_list, name="atelier-list"),
    path("atelier/<uuid:atelier_id>/", api_views.atelier_detail, name="atelier-detail"),
    path("atelier/<uuid:atelier_id>/star/", api_views.atelier_star, name="atelier-star"),

    # Experience endpoints
    path("experience/", api_views.experience_list, name="experience-list"),
    path("experience/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),

    # Skills endpoints
    path("skills/", api_views.skills_list, name="skills-list"),
    path("skills/<uuid:skills_id>/", api_views.skills_detail, name="skills-detail"),
]
