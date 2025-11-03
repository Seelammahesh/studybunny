from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    coins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Profile"


class Course(models.Model):
    title = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)  # or ForeignKey to User if you want
    credits = models.PositiveIntegerField(default=3)
    semester = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title


class Unit(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="units"
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Video(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="videos"
    )
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title


class PDFResource(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="pdfs"
    )
    title = models.CharField(max_length=255)
    url = models.URLField()  # or FileField if you want uploads

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes",
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.course.title if self.course else 'No Course'} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'✔' if self.is_correct else '✖'})"



class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    coins_earned = models.PositiveIntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"

    class Meta:
        ordering = ['-attempted_at']