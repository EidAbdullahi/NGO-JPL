from django import forms
from .models import Project, Workforce, Permit


# -------------------------
# Project Form
# -------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["ngo", "title", "description", "start_date", "end_date"]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


# -------------------------
# Workforce Form
# -------------------------
class WorkforceForm(forms.ModelForm):
    class Meta:
        model = Workforce
        fields = ["local_workers", "foreign_workers"]

        widgets = {
            "local_workers": forms.NumberInput(attrs={"min": 0}),
            "foreign_workers": forms.NumberInput(attrs={"min": 0}),
        }


# -------------------------
# Permit Form
# -------------------------
class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ["project", "permit_number", "issue_date", "expiry_date"]

        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }
