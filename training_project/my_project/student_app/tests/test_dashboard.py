
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from student_app.models import (
    Student,
    Department,
    Course,
    UserProfile
)


class DashboardTests(TestCase):

    # Test general dashboard totals, active students, and ORM reports.
    def test_general_dashboard_totals_and_orm_reports(self):
        department = Department.objects.create(
            name='Computer Science',
            description='IT Department'
        )

        Course.objects.create(
            course_name='Python',
            code='PY301',
            duration='3 Months'
        )

        Student.objects.create(
            name='Rahul',
            email='rahul@example.com',
            age=22,
            marks=80,
            joined_date=date.today(),
            department=department,
            is_active=True
        )

        Student.objects.create(
            name='Aman',
            email='aman@example.com',
            age=23,
            marks=60,
            joined_date=date.today(),
            department=department,
            is_active=False
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['active_students'], 1)
        self.assertEqual(response.context['total_departments'], 1)
        self.assertEqual(response.context['total_courses'], 1)
        self.assertEqual(response.context['average_marks'], 70)
        self.assertEqual(
            response.context['highest_student'].name,
            'Rahul'
        )

    # Test that the admin dashboard displays correct users and project totals.
    def test_admin_dashboard_totals(self):
        admin = User.objects.create_user(
            username='admin',
            password='Pass12345!'
        )

        UserProfile.objects.create(
            user=admin,
            role='admin'
        )

        trainer = User.objects.create_user(
            username='trainer',
            password='Pass12345!'
        )

        UserProfile.objects.create(
            user=trainer,
            role='trainer'
        )

        Department.objects.create(
            name='IT',
            description='IT Department'
        )

        Course.objects.create(
            course_name='Django',
            code='DJ301',
            duration='3 Months',
            trainer=trainer
        )

        Student.objects.create(
            name='Rahul',
            email='rahul@example.com',
            age=22,
            marks=75,
            joined_date=date.today()
        )

        self.client.login(
            username='admin',
            password='Pass12345!'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_users'], 2)
        self.assertEqual(response.context['total_students'], 1)
        self.assertEqual(response.context['total_courses'], 1)
        self.assertEqual(response.context['total_department'], 1)
        self.assertEqual(response.context['total_trainers'], 1)
