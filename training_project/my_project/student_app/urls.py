from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
     path('', views.student_list, name='student_list'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/', views.student_details, name='student_detail'),
    path('<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),
    # register
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Implemented Dashboard
    path('admin-dashboard/', views.admin_dashboard,name='admin_dashboard'),
    path('trainer-dashboard/', views.trainer_dashboard,name='trainer_dashboard'),
    path('student-dashboard/',views.student_dashboard,name='student_dashboard'),

    # password changes
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="students/registration/password_change.html",
            success_url="/students/"
        ),
        name="password_change"
),

    # reset Password 
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="students/registration/password_reset.html",
            email_template_name="students/registration/password_reset_email.txt",
            html_email_template_name="students/registration/password_reset_email.html",
            success_url="/students/password-reset/done/"
        ),
        name="password_reset"
),


    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="students/registration/password_reset_done.html"
        ),
        name="password_reset_done"
),

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="students/registration/password_reset_confirm.html",
            success_url="/students/password-reset/complete/"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="students/registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
    
]