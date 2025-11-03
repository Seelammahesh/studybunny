# lms/views.py

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages

from .models import (
    Course,
    StudentProfile,
    Quiz,
    Video,
    PDFResource,
    Choice,
    Attempt,
)
from .forms import (
    SignUpForm,
    LoginForm,
    CourseForm,
    VideoForm,
    PDFResourceForm,
    QuizForm,
)


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    courses = Course.objects.all()
    return render(request, "dashboard.html", {"courses": courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        "course": course,
        "units": course.units.all(),
        "videos": course.videos.all(),
        "pdfs": course.pdfs.all(),
        "quizzes": course.quizzes.all(),
        "sections": ["Units", "Videos", "PDFs", "Quizzes"],  
    }
    print(f'quizzes: {course.quizzes.all()}')
    return render(request, "courses_details.html", context=context)





@login_required
def leaderboard(request):
    leaders = StudentProfile.objects.select_related("user").order_by("-coins")
    return render(request, "leaderboard.html", {"leaders": leaders})


@login_required
def lectures(request):
    videos = Video.objects.all()
    pdfs = PDFResource.objects.all()
    return render(request, "lectures.html", {"videos": videos, "pdfs": pdfs})


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_list.html", {"quizzes": quizzes})


@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        correct = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected and q.choices.filter(id=selected, is_correct=True).exists():
                correct += 1
        score = int((correct / len(questions)) * 100)
        coins = 10 if score >= 80 else 5 if score >= 50 else 2
        attempt = Attempt.objects.create(user=request.user, quiz=quiz, score=score, coins_earned=coins)
        messages.success(request, f"You scored {score}% and earned {coins} coins! 🎉")
        return redirect("quiz_result", attempt.id)

    return render(request, "take_quiz.html", {"quiz": quiz, "questions": questions})

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user)
    return render(request, "quiz_result.html", {"attempt": attempt})


def is_staff_user(user):
    return user.is_staff


@user_passes_test(is_staff_user)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@user_passes_test(is_staff_user)
def admin_add_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = QuizForm()
    return render(
        request,
        "admin/admin_form.html",
        {"form": form, "title": "Add Quiz", "submit_label": "Create Quiz"},
    )


@user_passes_test(is_staff_user)
def admin_upload_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = VideoForm()
    return render(
        request,
        "admin/admin_form.html",
        {"form": form, "title": "Upload Video", "submit_label": "Upload"},
    )


@user_passes_test(is_staff_user)
def admin_upload_pdf(request):
    if request.method == "POST":
        form = PDFResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = PDFResourceForm()
    return render(
        request,
        "admin/admin_form.html",
        {"form": form, "title": "Upload PDF", "submit_label": "Upload"},
    )


@login_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")


class StudybunLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm


class StudybunLogoutView(LogoutView):
    next_page = reverse_lazy("index")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
