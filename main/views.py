from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render\

from main.models import Experience, Skills, Atelier
from main.forms import SkillsForm, ExperienceForm, AtelierForm


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
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experiences = [exp.object for exp in experiences] 
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aryan Alexander Rinaldi",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully added!")
        return redirect("main:show_experience")

    context = {"name": "Aryan A. Rinaldi", "form": form}
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted!")
    return redirect("main:show_experience")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    return HttpResponse(serializers.serialize("json", experiences), content_type="application/json")


# --- ATELIER VIEWS ---
def show_atelier(request):
    json_response = get_atelier_json(request)
    ateliers = serializers.deserialize("json", json_response.content.decode("utf-8"))
    ateliers = [item.object for item in ateliers] 
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aryan Alexander Rinaldi",
        "atelier_list": ateliers,
        "title_query": title_query,
    }
    return render(request, "atelier.html", context)

def create_atelier(request):
    form = AtelierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project successfully added!")
        return redirect("main:show_atelier")

    context = {"name": "Aryan A. Rinaldi", "form": form}
    return render(request, "atelier_form.html", context)

def delete_atelier(request, atelier_id):
    atelier = get_object_or_404(Atelier, pk=atelier_id)
    if request.method == "POST":
        atelier.delete()
        messages.success(request, "Project deleted!")
    return redirect("main:show_atelier")

def get_atelier_json(request):
    title_query = request.GET.get("title", "").strip()
    ateliers = Atelier.objects.all()
    if title_query:
        ateliers = ateliers.filter(title__icontains=title_query)
    return HttpResponse(serializers.serialize("json", ateliers), content_type="application/json")

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