from django.urls import path
from . import views

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
]