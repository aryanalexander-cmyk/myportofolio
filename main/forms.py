from django.forms import ModelForm, TextInput, Textarea
from main.models import Skills

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