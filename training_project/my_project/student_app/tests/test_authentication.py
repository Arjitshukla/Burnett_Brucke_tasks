
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import date
from student_app.models import (
    UserProfile,
    AuditLog,
)


class AuthenticationTests(TestCase):

    # Test that the login page loads successfully.
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    # Test that the registration page loads successfully.
    def test_registration_page_loads(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    # Test that login fails when invalid credentials are provided.
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

    # Test that a student can log in and is redirected to the student dashboard.
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

    # Test that a failed login increases the user's failed attempt count.
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

    # Test that successful login resets failed attempts and unlocks the account.
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

    # Test that the account gets locked after five failed login attempts.
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

    # Test that a locked account cannot log in with correct credentials.
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

    # Test that successful login creates a LOGIN audit log entry.
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

    # Test that failed login creates a FAILED audit log entry.
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
