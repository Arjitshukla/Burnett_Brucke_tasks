from django.urls import path
from . import views

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [

    # ==========================================
    # 1. STUDENT CRUD OPERATIONS
    # ==========================================

    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/', views.student_details, name='student_detail'),
    path('<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),


    # ==========================================
    # 2. USER AUTHENTICATION & REGISTRATION
    # ==========================================

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # ==========================================
    # 3. GENERAL DASHBOARD
    # ==========================================

    path('dashboard/', views.dashboard, name='dashboard'),

    # ==========================================
    # 4. ADMIN DASHBOARD & USER MANAGEMENT
    # ==========================================

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path(
        'admin/user-status/<int:user_id>/',
        views.toggle_user_status,
        name='toggle_user_status'
    ),


    # ==========================================
    # 5. ADMIN FEEDBACK MANAGEMENT
    # ==========================================

    path(
        'admin/all-feedback/',
        views.all_feedback_view,
        name='all_feedback'
    ),

    path(
        'admin/feedback/visibility/<int:feedback_id>/',
        views.toggle_feedback_visibility,
        name='toggle_feedback_visibility'
    ),


    # ==========================================
    # 6. ADMIN AUDIT LOGS & MARKS HISTORY
    # ==========================================

    path('audit-logs/', views.audit_logs_view, name='audit_logs'),

    path(
        'admin/marks-history/',
        views.marks_history_view,
        name='marks_history'
    ),


    # ==========================================
    # 7. TRAINER DASHBOARD & FEEDBACK MANAGEMENT
    # ==========================================

    path(
        'trainer-dashboard/',
        views.trainer_dashboard,
        name='trainer_dashboard'
    ),

    path(
        'trainer/feedback/<int:student_id>/',
        views.give_feedback,
        name='give_feedback'
    ),

    path(
        'trainer/feedback/edit/<int:feedback_id>/',
        views.edit_feedback,
        name='edit_feedback'
    ),


    # ==========================================
    # 8. TRAINER MARKS MANAGEMENT
    # ==========================================

    path(
        'trainer/update-marks/<int:student_id>/<int:course_id>/',
        views.update_course_marks,
        name='update_course_marks'
    ),


    # ==========================================
    # 9. STUDENT DASHBOARD
    # ==========================================

    path(
        'student-dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),


    # ==========================================
    # 10. PASSWORD CHANGE
    # ==========================================

    path(
        'change-password/',
        PasswordChangeView.as_view(
            template_name='students/registration/password_change.html',
            success_url='/students/'
        ),
        name='password_change'
    ),


    # ==========================================
    # 11. PASSWORD RESET WORKFLOW
    # ==========================================

    path(
        'password-reset/',
        PasswordResetView.as_view(
            template_name='students/registration/password_reset.html',
            email_template_name='students/registration/password_reset_email.txt',
            html_email_template_name='students/registration/password_reset_email.html',
            success_url='/students/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='students/registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='students/registration/password_reset_confirm.html',
            success_url='/students/reset/done/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='students/registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]