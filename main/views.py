from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        
from django.shortcuts import get_object_or_404, redirect, render


from main.models import Experience, Skills, Atelier
from main.forms import SkillsForm, ExperienceForm, AtelierForm


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Aryan Alexander Rinaldi",
        "npm": "2506636985",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "Art student larping as a CS Student @ Fakultas Ilmu Komputer Univ. Indonesia. Spends far too much on toy robots."
        ),
        "last_login": last_login,
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

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully added!")
        return redirect("main:show_experience")

    context = {"name": "Aryan A. Rinaldi", "form": form}
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def create_atelier(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = AtelierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project successfully added!")
        return redirect("main:show_atelier")

    context = {"name": "Aryan A. Rinaldi", "form": form}
    return render(request, "atelier_form.html", context)

@login_required(login_url="/login/")
def delete_atelier(request, atelier_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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
        "json", ateliers, use_natural_foreign_keys=True
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

@login_required(login_url="/login/")
def delete_skills(request, skills_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    skills = get_object_or_404(Skills, pk=skills_id)

    if request.method == "POST":
        skills.delete()
        messages.success(request, "Skill succesfully deleted!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

@login_required(login_url="/login/")

def create_skills(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account succesfully created. Please continue to the login page.")
        return redirect("main:login")

    context = {
        "name": "Aryan A. Rinaldi",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Aryan A. Rinaldi",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, atelier_id):
    project = get_object_or_404(Atelier, pk=atelier_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_atelier")