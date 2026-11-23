from django.urls import path
# from . import views
from .views.auth_views import (
    register_view,
    login_view,
    logout_view,
)

from .views.student_views import (
    student_list,
    add_student,
    student_details,
    edit_student,
    delete_student,
    student_dashboard,
    dashboard
)

from .views.admin_views import (
    admin_dashboard,
    toggle_feedback_visibility,
    toggle_user_status,
    audit_logs_view,
    all_feedback_view,
    marks_history_view,
)

from .views.trainer_views import (
    trainer_dashboard,
    give_feedback,
    update_course_marks,
    edit_feedback,
)

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

    path('', student_list, name='student_list'),
    path('add/', add_student, name='add_student'),
    path('<int:pk>/', student_details, name='student_detail'),
    path('<int:pk>/edit/', edit_student, name='edit_student'),
    path('<int:pk>/delete/', delete_student, name='delete_student'),


    # ==========================================
    # 2. USER AUTHENTICATION & REGISTRATION
    # ==========================================

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    # ==========================================
    # 3. GENERAL DASHBOARD
    # ==========================================

    path('dashboard/',
          dashboard,
            name='dashboard'),

    # ==========================================
    # 4. ADMIN DASHBOARD & USER MANAGEMENT
    # ==========================================

    path('admin-dashboard/',
          admin_dashboard,
            name='admin_dashboard'),

    path('admin/user-status/<int:user_id>/',
        toggle_user_status,
          name='toggle_user_status'),


    # ==========================================
    # 5. ADMIN FEEDBACK MANAGEMENT
    # ==========================================

    path('admin/all-feedback/',
          all_feedback_view,
            name='all_feedback'),

    path('admin/feedback/visibility/<int:feedback_id>/',
          toggle_feedback_visibility, 
          name='toggle_feedback_visibility'),


    # ==========================================
    # 6. ADMIN AUDIT LOGS & MARKS HISTORY
    # ==========================================

    path('audit-logs/',
          audit_logs_view,
          name='audit_logs'),

    path('admin/marks-history/',
          marks_history_view,
            name='marks_history'),


    # ==========================================
    # 7. TRAINER DASHBOARD & FEEDBACK MANAGEMENT
    # ==========================================

    path('trainer-dashboard/',
          trainer_dashboard,
            name='trainer_dashboard'),

    path('trainer/feedback/<int:student_id>/',
          give_feedback,
            name='give_feedback'),

    path('trainer/feedback/edit/<int:feedback_id>/',
          edit_feedback,
            name='edit_feedback'),


    # ==========================================
    # 8. TRAINER MARKS MANAGEMENT
    # ==========================================

    path('trainer/update-marks/<int:student_id>/<int:course_id>/',
          update_course_marks,
         name='update_course_marks'),


    # ==========================================
    # 9. STUDENT DASHBOARD
    # ==========================================

    path('student-dashboard/',
        student_dashboard,
        name='student_dashboard'),


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