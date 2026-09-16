from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render\

from main.models import Experience
from main.models import Skills
from main.forms import SkillsForm


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

def show_atelier(request):
    context = {
        "name": "Aryan Alexander Rinaldi",
    }
    return render(request, "atelier.html", context)

def show_skills(request):
    json_response = get_skills_json(request)

    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills] 
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aryan Alexander Rinaldi",
        "skills_list": skills,
        "title_query": title_query,
    }
    # Fixed: render the correct template
    return render(request, "skills.html", context)

def delete_skills(request, skills_id):
    skills = get_object_or_404(Skills, pk=skills_id)

    if request.method == "POST":
        skills.delete()
        messages.success(request, "Skill succesfully deleted!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

def create_skills(request):
    form = SkillsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New skill succesfully added!")
        return redirect("main:show_skills")

    context = {
        "name": "Aryan A. Rinaldi",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def get_skills_json(request):
    title_query = request.GET.get("title", "").strip()
    skills = Skills.objects.all()

    if title_query:
        skills = skills.filter(title__icontains=title_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")