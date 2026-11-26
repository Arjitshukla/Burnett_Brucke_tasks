
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from student_app.models import (
    UserProfile,
    Student,
    Course,
)


class PermissionTests(TestCase):

    # Test 11: Verify that a student cannot access the admin dashboard.
    def test_student_cannot_access_admin_dashboard(self):
        user = User.objects.create_user(
            username='studentuser',
            password='CorrectPass123!'
        )

        UserProfile.objects.create(
            user=user,
            role='student'
        )

        self.client.login(
            username='studentuser',
            password='CorrectPass123!'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 403)

    # Test 12: Verify that a trainer cannot access the admin dashboard.
    def test_trainer_cannot_access_admin_dashboard(self):
        user = User.objects.create_user(
            username='traineruser',
            password='CorrectPass123!'
        )
        UserProfile.objects.create(user=user, role='trainer')

        self.client.login(
            username='traineruser',
            password='CorrectPass123!'
        )

        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 403)

    # Test 13: Verify that a student cannot view another student's details.
    def test_student_cannot_view_another_student(self):
        user1 = User.objects.create_user(username='student1', password='Pass12345!')
        user2 = User.objects.create_user(username='student2', password='Pass12345!')

        UserProfile.objects.create(user=user1, role='student')
        UserProfile.objects.create(user=user2, role='student')

        other_student = Student.objects.create(
            user=user2,
            name='Other Student',
            email='other@example.com',
            age=22,
            marks=75,
            joined_date=date.today()
        )

        self.client.login(username='student1', password='Pass12345!')

        response = self.client.get(
            reverse('student_detail', args=[other_student.id])
        )

        self.assertEqual(response.status_code, 404)

    # Test 14: Verify that a trainer cannot update marks of an unassigned student.
    def test_trainer_cannot_update_unassigned_student_marks(self):
        trainer = User.objects.create_user(
            username='trainer1',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=trainer, role='trainer')

        course = Course.objects.create(
            course_name='Python',
            code='PY101',
            duration='3 Months',
            trainer=trainer
        )

        student = Student.objects.create(
            name='Test Student',
            email='test@example.com',
            age=22,
            marks=70,
            joined_date=date.today()
        )

        self.client.login(username='trainer1', password='Pass12345!')

        response = self.client.get(
            reverse(
                'update_course_marks',
                args=[student.id, course.id]
            )
        )

        self.assertEqual(response.status_code, 404)

    # Test 15: Verify that a student cannot update marks using a direct POST request.
    def test_student_cannot_update_marks_through_post(self):
        student_user = User.objects.create_user(
            username='studentuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=student_user, role='student')

        course = Course.objects.create(
            course_name='Django',
            code='DJ101',
            duration='3 Months'
        )

        student = Student.objects.create(
            user=student_user,
            name='Test Student',
            email='test@example.com',
            age=22,
            marks=70,
            joined_date=date.today()
        )
        student.courses.add(course)

        self.client.login(
            username='studentuser',
            password='Pass12345!'
        )

        response = self.client.post(
            reverse('update_course_marks', args=[student.id, course.id]),
            {'marks': 90, 'reason': 'Test update'}
        )

        self.assertEqual(response.status_code, 403)

    # Test 16: Verify that an admin can access the all-feedback page.
    def test_admin_can_view_all_feedback(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=admin, role='admin')

        self.client.login(username='adminuser', password='Pass12345!')

        response = self.client.get(reverse('all_feedback'))

        self.assertEqual(response.status_code, 200)

    # Test 17: Verify that a student cannot access the all-feedback page.
    def test_student_cannot_view_all_feedback(self):
        user = User.objects.create_user(
            username='studentuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=user, role='student')

        self.client.login(username='studentuser', password='Pass12345!')

        response = self.client.get(reverse('all_feedback'))

        self.assertEqual(response.status_code, 403)

    # Test 18: Verify that an admin can access the marks history page.
    def test_admin_can_view_marks_history(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=admin, role='admin')

        self.client.login(username='adminuser', password='Pass12345!')

        response = self.client.get(reverse('marks_history'))

        self.assertEqual(response.status_code, 200)

    # Test 19: Verify that a trainer cannot access the marks history page.
    def test_trainer_cannot_view_marks_history(self):
        trainer = User.objects.create_user(
            username='traineruser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=trainer, role='trainer')

        self.client.login(username='traineruser', password='Pass12345!')

        response = self.client.get(reverse('marks_history'))

        self.assertEqual(response.status_code, 403)
