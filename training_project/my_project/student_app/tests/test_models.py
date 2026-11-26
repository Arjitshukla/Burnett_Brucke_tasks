
from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User
from student_app.models import Student, Course, UserProfile, CourseMarks


class StudentModelTests(TestCase):

    # Test that a student record is created and saved successfully.
    def test_student_creation(self):
        student = Student.objects.create(
            name='Rahul Sharma',
            email='rahul@example.com',
            age=22,
            marks=85,
            joined_date=date.today()
        )

        self.assertEqual(student.name, 'Rahul Sharma')
        self.assertEqual(student.email, 'rahul@example.com')
        self.assertEqual(student.age, 22)
        self.assertEqual(student.marks, 85)
        self.assertTrue(
            Student.objects.filter(id=student.id).exists()
        )

    # Test that the student model returns the student's name as its string representation.
    def test_student_string_representation(self):
        student = Student.objects.create(
            name='Rahul Sharma',
            email='rahul@example.com',
            age=22,
            marks=85,
            joined_date=date.today()
        )

        self.assertEqual(str(student), 'Rahul Sharma')

    # Test that a course is created with the correct details and assigned trainer.
    def test_course_creation(self):
        trainer = User.objects.create_user(
            username='trainer1',
            password='Pass12345!'
        )

        UserProfile.objects.create(
            user=trainer,
            role='trainer'
        )

        course = Course.objects.create(
            course_name='Python',
            code='PY101',
            duration='3 Months',
            trainer=trainer
        )

        self.assertEqual(course.course_name, 'Python')
        self.assertEqual(course.code, 'PY101')
        self.assertEqual(course.trainer, trainer)
        self.assertTrue(
            Course.objects.filter(id=course.id).exists()
        )

    # Test that a user profile is created with the correct user and role.
    def test_user_profile_creation(self):
        user = User.objects.create_user(
            username='student1',
            password='Pass12345!'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student'
        )

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.role, 'student')
        self.assertTrue(
            UserProfile.objects.filter(user=user).exists()
        )

    # Test that course marks are created and linked to the correct student and course.
    def test_course_marks_creation(self):
        trainer = User.objects.create_user(
            username='trainer2',
            password='Pass12345!'
        )

        UserProfile.objects.create(
            user=trainer,
            role='trainer'
        )

        course = Course.objects.create(
            course_name='Django',
            code='DJ101',
            duration='3 Months',
            trainer=trainer
        )

        student = Student.objects.create(
            name='Aman Sharma',
            email='aman@example.com',
            age=22,
            marks=75,
            joined_date=date.today()
        )

        student.courses.add(course)

        course_marks = CourseMarks.objects.create(
            student=student,
            course=course,
            marks=85
        )

        self.assertEqual(course_marks.student, student)
        self.assertEqual(course_marks.course, course)
        self.assertEqual(course_marks.marks, 85)
        self.assertTrue(
            CourseMarks.objects.filter(id=course_marks.id).exists()
        )
