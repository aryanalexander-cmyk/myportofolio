from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Aryan Alexander Rinaldi",
        "npm": "2506636985",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "Art student larping as a CS Student @ Fakultas Ilmu Komputer Univ. Indonesia. Spends far too much on toy robots."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aryan Alexander Rinaldi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)