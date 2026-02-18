from django import forms
from .models import Project, Task
from datetime import date


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "deadline", "status", "priority"]
        widgets = {"deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"})}

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < date.today():
            raise forms.ValidationError("Deadline cannot be in the past")
        return deadline
