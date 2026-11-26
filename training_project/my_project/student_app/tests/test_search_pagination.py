
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from student_app.models import Student, UserProfile


class StudentSearchPaginationTests(TestCase):

    # Create an admin user and log in before running each test.
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='Pass12345!'
        )

        UserProfile.objects.create(
            user=self.admin,
            role='admin'
        )

        self.client.login(
            username='admin',
            password='Pass12345!'
        )

    # Create a student record with the given details for testing.
    def create_student(self, name, email, marks, active=True):
        return Student.objects.create(
            name=name,
            email=email,
            age=22,
            marks=marks,
            joined_date=date.today(),
            is_active=active
        )

    # Test that student pagination displays the correct records on page 2.
    def test_student_list_pagination(self):
        for i in range(12):
            self.create_student(
                name=f'Student {i}',
                email=f'student{i}@example.com',
                marks=70
            )

        response = self.client.get(
            reverse('student_list'),
            {'page': 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertEqual(len(response.context['page_obj'].object_list), 2)
        self.assertTrue(response.context['page_obj'].has_previous())

    # Test that search, active status, and pass-result filters work together.
    def test_student_search_with_status_and_result_filters(self):
        self.create_student(
            'Rahul Sharma',
            'rahul@example.com',
            85,
            True
        )

        self.create_student(
            'Rahul Verma',
            'rahul2@example.com',
            30,
            True
        )

        self.create_student(
            'Rahul Gupta',
            'rahul3@example.com',
            90,
            False
        )

        self.create_student(
            'Aman Sharma',
            'aman@example.com',
            90,
            True
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'search': 'Rahul',
                'status': 'active',
                'result': 'pass'
            }
        )

        self.assertEqual(response.status_code, 200)

        students = response.context['page_obj'].object_list

        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, 'Rahul Sharma')
