from django import forms
from django.contrib.auth.models import User
from .models import Job, Application, Profile

# class RegistrationForm(forms.ModelForm):
#     ROLE_CHOICES = (
#         ("EMPLOYER", "Employer"),
#         ("APPLICANT", "Applicant"),
#     )
#     password = forms.CharField(widget=forms.PasswordInput)
#     role = forms.ChoiceField(choices=ROLE_CHOICES)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#             Profile.objects.update_or_create(user=user, defaults={"role": self.cleaned_data["role"]})
#         return user

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
        ("EMPLOYER", "Employer"),
        ("APPLICANT", "Applicant"),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={"role": self.cleaned_data["role"]}
            )
        return user


from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company_name", "location", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            "company_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            "location": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location'
            }),
            "description": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the job role...',
                'rows': 4
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]
        widgets = {
            "resume": forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            "cover_letter": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your cover letter...',
                'rows': 4
            }),
        }


# class JobForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ["title", "company_name", "location", "description"]


# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ["resume", "cover_letter"]
