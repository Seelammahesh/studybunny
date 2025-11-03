# lms/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Course, Video, PDFResource, Quiz

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "class": "form-control",
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Choose a username",
                "class": "form-control",
            }),
            "password1": forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            "password2": forms.PasswordInput(attrs={
                "placeholder": "Confirm password",
                "class": "form-control",
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your username",
            "class": "form-control",
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "form-control",
        })
    )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "faculty", "credits", "semester"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "faculty": forms.TextInput(attrs={"class": "form-control"}),
            "credits": forms.NumberInput(attrs={"class": "form-control"}),
            "semester": forms.TextInput(attrs={"class": "form-control"}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["course", "title", "url"]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
        }


class PDFResourceForm(forms.ModelForm):
    class Meta:
        model = PDFResource
        fields = ["course", "title", "url"]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", ]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "max_score": forms.NumberInput(attrs={"class": "form-control"}),
            "coins_reward": forms.NumberInput(attrs={"class": "form-control"}),
        }
