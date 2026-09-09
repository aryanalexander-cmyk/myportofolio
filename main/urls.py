from django.urls import path

from main.views import show_main, show_experience, show_atelier

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),\
    path("atelier/", show_atelier, name="show_atelier"),
]