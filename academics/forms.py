from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["valeur"]
        widgets = {
            "valeur": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0",
                "max": "20",
                "class": "form-input",
            })
        }