# lms/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),

    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("lectures/", views.lectures, name="lectures"),

    path("/quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("quiz/attempt/<int:attempt_id>/", views.quiz_result, name="quiz_result"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/quiz/add/", views.admin_add_quiz, name="admin_add_quiz"),
    path("admin-dashboard/video/upload/", views.admin_upload_video, name="admin_upload_video"),
    path("admin-dashboard/pdf/upload/", views.admin_upload_pdf, name="admin_upload_pdf"),

    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),

    path("login/", views.StudybunLoginView.as_view(), name="login"),
    path("logout/", views.StudybunLogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
]
