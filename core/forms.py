from django import forms
from django.core.exceptions import ValidationError
from .models import NGO, Project, Workforce, Worker, Permit

# -------------------------
# NGO Form
# -------------------------
class NGOForm(forms.ModelForm):
    class Meta:
        model = NGO
        fields = [
            'name', 'description', 'email', 'phone_number', 'address',
            'area_manager', 'website', 'profile_picture'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NGO Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
            'area_manager': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area Manager'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

# -------------------------
# Project Form
# -------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["ngo", "title", "description", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ngo": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and end < start:
            raise ValidationError("End date cannot be earlier than start date.")
        return cleaned_data

# -------------------------
# Workforce Form
# -------------------------
class WorkforceForm(forms.ModelForm):
    class Meta:
        model = Workforce
        fields = ["local_workers", "foreign_workers"]
        widgets = {
            "local_workers": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
            "foreign_workers": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        local = cleaned_data.get("local_workers", 0)
        foreign = cleaned_data.get("foreign_workers", 0)
        if local < 0 or foreign < 0:
            raise ValidationError("Worker counts cannot be negative.")
        return cleaned_data

# -------------------------
# Worker Form
# -------------------------
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'email', 'phone_number', 'salary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Worker Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
        }

# -------------------------
# Permit Form
# -------------------------
class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ["project", "permit_number", "permit_type", "issue_date", "expiry_date", "workers"]
        widgets = {
            "project": forms.Select(attrs={"class": "form-select"}),
            "permit_number": forms.TextInput(attrs={"class": "form-control"}),
            "permit_type": forms.Select(attrs={"class": "form-select"}),
            "issue_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "expiry_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "workers": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        issue = cleaned_data.get("issue_date")
        expiry = cleaned_data.get("expiry_date")
        if issue and expiry and expiry < issue:
            raise ValidationError("Expiry date cannot be earlier than issue date.")
        return cleaned_data
