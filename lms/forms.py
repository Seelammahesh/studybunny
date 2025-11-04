# lms/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Course, Video, PDFResource, Quiz

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("full_name", "email", "password1", "password2")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
        }

    

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email"
    }))

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
