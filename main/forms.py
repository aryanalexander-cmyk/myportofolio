from django.forms import ModelForm, TextInput, Textarea
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from main.models import Experience, Skills, Atelier

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]
        labels = {
            "title": "Experience Title",
            "description": "Description",
            "category": "Category",
            "ended_at": "End Date (Leave blank if ongoing)",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "e.g., Software Engineer Intern", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Describe your role", "rows": 3}),
        }

class AtelierForm(ModelForm):
    class Meta:
        model = Atelier
        fields = ["title", "project_url", "image_url"]
        labels = {
            "title": "Project Title",
            "project_url": "Project Link",
            "image_url": "Thumbnail Image URL",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "e.g., Destructon", "maxlength": 255}),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Project name can't contain only HTML tags.")
        return title
        
    def clean_project_url(self):
        url = self.cleaned_data.get("project_url", "")
        if url:
            return strip_tags(url).strip()
        return url

    def clean_image_url(self):
        url = self.cleaned_data.get("image_url", "")
        if url:
            return strip_tags(url).strip()
        return url

class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = [
            "title",
            "description",
            "type",
        ]

        labels = {
            "title": "Skill Name",
            "description": "Skill Description",
            "type": "Type of Skill",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "What's your chosen skill?",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your skills!",
                    "rows": 3,
                }
            ),
            "type": TextInput(
                attrs={
                    "placeholder": "Programming, Design, Art, Writing, Baking",
                }
            ),
            
        }