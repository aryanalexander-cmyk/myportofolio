from django.forms import ModelForm, TextInput, Textarea
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