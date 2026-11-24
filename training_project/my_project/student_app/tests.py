from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import date
from student_app.models import (
    UserProfile,
    AuditLog,
    Student,
    Course,
    CourseMarks,
)


class AuthenticationTests(TestCase):

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    
    def test_registration_page_loads(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    
    
    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'wronguser',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            '_auth_user_id',
            self.client.session
        )


    def test_valid_student_login(self):
        user = User.objects.create_user(
            username='teststudent',
            password='Test@12345'
        )

        UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'student'}
        )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'teststudent',
                'password': 'Test@12345'
            }
        )

        self.assertRedirects(
            response,
            reverse('student_dashboard'),
            fetch_redirect_response=False
        )

        self.assertEqual(
            self.client.session['_auth_user_id'],
            str(user.pk)
        )

    def test_failed_login_increases_attempt_count(self):
        user = User.objects.create_user(
            username='testuser',
            password='CorrectPass123!'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student'
        )

        self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'WrongPassword123!'
            }
        )

        profile.refresh_from_db()

        self.assertEqual(profile.failed_login_attempts, 1)
        self.assertIsNone(profile.locked_until)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_successful_login_resets_failed_attempts(self):
        user = User.objects.create_user(
            username='testuser',
            password='CorrectPass123!'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student',
            failed_login_attempts=2
        )

        self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'CorrectPass123!'
            }
        )

        profile.refresh_from_db()

        self.assertEqual(profile.failed_login_attempts, 0)
        self.assertIsNone(profile.locked_until)
        self.assertIn('_auth_user_id', self.client.session)

    # Test 7: Account Lock After 5 Failed Attempts
    def test_account_locks_after_five_failed_attempts(self):
        user = User.objects.create_user(
            username='testuser',
            password='CorrectPass123!'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student'
        )

        for _ in range(5):
            self.client.post(
                reverse('login'),
                {
                    'username': 'testuser',
                    'password': 'WrongPassword123!'
                }
            )

        profile.refresh_from_db()

        self.assertEqual(profile.failed_login_attempts, 5)
        self.assertIsNotNone(profile.locked_until)
        self.assertGreater(profile.locked_until, timezone.now())
        self.assertNotIn('_auth_user_id', self.client.session)

    # Test 8: Locked Account Cannot Login

    def test_locked_account_cannot_login(self):
        user = User.objects.create_user(
            username='lockeduser',
            password='CorrectPass123!'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student',
            failed_login_attempts=5,
            locked_until=timezone.now() + timedelta(minutes=15)
        )

        self.client.post(
            reverse('login'),
            {
                'username': 'lockeduser',
                'password': 'CorrectPass123!'
            }
        )

        profile.refresh_from_db()

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(profile.failed_login_attempts, 5)
        self.assertIsNotNone(profile.locked_until)

    # Test 9: Successful Login Creates Audit Log.
    def test_successful_login_creates_audit_log(self):
        user = User.objects.create_user(
            username='audituser',
            password='CorrectPass123!'
        )

        UserProfile.objects.create(
            user=user,
            role='student'
        )

        self.client.post(
            reverse('login'),
            {
                'username': 'audituser',
                'password': 'CorrectPass123!'
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                username='audituser',
                event='LOGIN'
            ).exists()
        )

    # Test 10: Failed Login Creates Audit Log
    def test_failed_login_creates_audit_log(self):
        user = User.objects.create_user(
            username='faileduser',
            password='CorrectPass123!'
        )

        UserProfile.objects.create(
            user=user,
            role='student'
        )

        self.client.post(
            reverse('login'),
            {
                'username': 'faileduser',
                'password': 'WrongPassword123!'
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                username='faileduser',
                event='FAILED'
            ).exists()
        )

    # Test 11: Student Cannot Access Admin Dashboard
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

    # Test 12 — Trainer cannot access Admin Dashboard
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

    # Test 13 — Student cannot view another student's details
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

    # Test 14 — Trainer cannot update marks of an unassigned student
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

    # Test 15 — Student cannot update marks through direct POST
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

    # Test 16 — Admin can view all feedback
    def test_admin_can_view_all_feedback(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=admin, role='admin')

        self.client.login(username='adminuser', password='Pass12345!')

        response = self.client.get(reverse('all_feedback'))

        self.assertEqual(response.status_code, 200) 

    # Test 17 — Student cannot view all feedback
    def test_student_cannot_view_all_feedback(self):
        user = User.objects.create_user(
            username='studentuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=user, role='student')

        self.client.login(username='studentuser', password='Pass12345!')

        response = self.client.get(reverse('all_feedback'))

        self.assertEqual(response.status_code, 403)

    # Test 18 — Admin can view marks history
    def test_admin_can_view_marks_history(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=admin, role='admin')

        self.client.login(username='adminuser', password='Pass12345!')

        response = self.client.get(reverse('marks_history'))

        self.assertEqual(response.status_code, 200)

    # Test 19 — Trainer cannot view marks history
    def test_trainer_cannot_view_marks_history(self):
        trainer = User.objects.create_user(
            username='traineruser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=trainer, role='trainer')

        self.client.login(username='traineruser', password='Pass12345!')

        response = self.client.get(reverse('marks_history'))

        self.assertEqual(response.status_code, 403)

    # Test 20 — Marks above 100 are rejected
    def test_marks_above_100_are_rejected(self):
        trainer = User.objects.create_user(
            username='traineruser',
            password='Pass12345!'
        )
        UserProfile.objects.create(user=trainer, role='trainer')

        course = Course.objects.create(
            course_name='Python',
            code='PY102',
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
        student.courses.add(course)

        self.client.login(username='traineruser', password='Pass12345!')

        response = self.client.post(
            reverse('update_course_marks', args=[student.id, course.id]),
            {'marks': 150, 'reason': 'Invalid marks test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            CourseMarks.objects.filter(student=student, course=course).exists()
        )