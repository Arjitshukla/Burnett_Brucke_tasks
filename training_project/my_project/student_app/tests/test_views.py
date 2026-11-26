from django.test import TestCase
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

from student_app.models import (
    UserProfile,
    Student,
    Course,
    CourseMarks,
)


class ViewTests(TestCase):

    # Verify that the trainer cannot assign marks greater than 100 to a student.
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