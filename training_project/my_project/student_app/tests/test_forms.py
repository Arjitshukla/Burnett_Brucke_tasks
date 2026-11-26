
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from student_app.models import Student, Course, UserProfile
from student_app.forms import StudentForm, FeedbackForm, CourseMarksForm


class StudentFormTests(TestCase):

    def test_student_form_with_valid_data(self):
        form = StudentForm(data={
            'name': 'Rahul Sharma',
            'email': 'rahul@example.com',
            'age': 22,
            'marks': 85,
            'joined_date': date.today().isoformat(),
            'is_active': 'on',
        })

        self.assertTrue(form.is_valid())

    def test_student_form_rejects_invalid_age(self):
        form = StudentForm(data={
            'name': 'Rahul Sharma',
            'email': 'rahul@example.com',
            'age': 15,
            'marks': 85,
            'joined_date': date.today().isoformat(),
            'is_active': 'on',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)


class FeedbackFormTests(TestCase):

    def setUp(self):
        self.trainer = User.objects.create_user(
            username='trainer',
            password='Pass12345!'
        )

        self.course = Course.objects.create(
            course_name='Python',
            code='PY201',
            duration='3 Months',
            trainer=self.trainer
        )

    def test_feedback_form_with_valid_data(self):
        form = FeedbackForm(data={
            'course': self.course.id,
            'rating': 5,
            'message': 'Excellent teaching!'
        })

        self.assertTrue(form.is_valid())

    def test_feedback_form_rejects_invalid_rating(self):
        form = FeedbackForm(data={
            'course': self.course.id,
            'rating': 6,
            'message': 'Good course'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)


class CourseMarksFormTests(TestCase):

    def test_course_marks_form_with_valid_data(self):
        form = CourseMarksForm(data={
            'marks': 85,
            'reason': 'Monthly assessment'
        })

        self.assertTrue(form.is_valid())

    def test_course_marks_form_rejects_marks_above_100(self):
        form = CourseMarksForm(data={
            'marks': 150,
            'reason': 'Invalid marks'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('marks', form.errors)
