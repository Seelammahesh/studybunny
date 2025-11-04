from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model


# -----------------------------
# Custom User Model
# -----------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_student = models.BooleanField(default=True, null=True, blank=True)
    is_teacher = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.username or "User"


# Make sure User points to the custom one
User = get_user_model()


# -----------------------------
# Student Profile
# -----------------------------
class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True,
    )
    coins = models.PositiveIntegerField(default=0, null=True, blank=True)
    enrolled_courses = models.ManyToManyField(
        "Course", blank=True, related_name="students"
    )

    def __str__(self):
        return f"{self.user.full_name or self.user.email} Profile"


# -----------------------------
# Course Models
# -----------------------------
class Course(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_taught",
    )
    credits = models.PositiveIntegerField(default=3, null=True, blank=True)
    semester = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Course"


class Unit(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="units",
        null=True, blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1, null=True, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title if self.course else 'No Course'} - {self.title}"


# -----------------------------
# Resources (Videos, PDFs)
# -----------------------------
class Video(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="videos",
        null=True, blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Video"


class PDFResource(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="pdfs",
        null=True, blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled PDF"


# -----------------------------
# Quiz Models
# -----------------------------
class Quiz(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="quizzes",
        null=True, blank=True
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course.title if self.course else 'No Course'} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE,
        null=True, blank=True
    )
    text = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.quiz.title if self.quiz else 'No Quiz'} - {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE,
        null=True, blank=True
    )
    text = models.CharField(max_length=300, null=True, blank=True)
    is_correct = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.text or 'Choice'} ({'✔' if self.is_correct else '✖'})"


# -----------------------------
# Attempts
# -----------------------------
class Attempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='attempts',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quiz = models.ForeignKey(
        Quiz, related_name='attempts', on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    score = models.PositiveIntegerField(default=0, null=True, blank=True)
    coins_earned = models.PositiveIntegerField(default=0, null=True, blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email if self.user else 'No User'} - {self.quiz.title if self.quiz else 'No Quiz'} ({self.score}%)"

    class Meta:
        ordering = ['-attempted_at']
