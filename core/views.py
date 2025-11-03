from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Quiz, StudentProfile, QuizAttempt

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('courses_details')  # **Redirects to /courses/**
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

@login_required
def courses_details(request):
    return render(request, 'courses_details.html')

@login_required
def student_dashboard(request):
    quizzes = Quiz.objects.all()
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'student_dashboard.html', {
        'quizzes': quizzes,
        'coins': student_profile.coins,
    })

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            choice_id = request.POST.get(str(question.id))
            if choice_id:
                choice = quiz.choices.filter(id=choice_id, question=question).first()
                if choice and choice.is_correct:
                    score += 1
        coins = score * 2
        student_profile = StudentProfile.objects.get(user=request.user)
        student_profile.coins += coins
        student_profile.save()
        QuizAttempt.objects.create(student=student_profile, quiz=quiz, score=score, coins_earned=coins)
        return redirect('quiz_result', quiz_id=quiz.id)
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, quiz_id):
    student_profile = StudentProfile.objects.get(user=request.user)
    attempts = QuizAttempt.objects.filter(student=student_profile, quiz_id=quiz_id).order_by('-date_taken')
    attempt = attempts.first() if attempts.exists() else None
    return render(request, 'quiz_result.html', {'attempt': attempt})

@login_required
def leaderboard(request):
    leaders = StudentProfile.objects.order_by('-coins')[:10]
    return render(request, 'leaderboard.html', {'leaders': leaders})
