from django.contrib import admin
from .models import (
    StudentProfile,
    Course,
    Unit,
    Video,
    PDFResource,
    Quiz,
    Question,
    Choice,
    Attempt,
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "coins")
    search_fields = ("user__username",)


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class PDFInline(admin.TabularInline):
    model = PDFResource
    extra = 1

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "faculty", "credits", "semester")
    search_fields = ("title", "faculty")
    inlines = [UnitInline, VideoInline, PDFInline, QuizInline]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [ChoiceInline]

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'coins_earned', 'attempted_at')
    list_filter = ('quiz', 'user')