
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from student_app.models import (
    UserProfile,
    Department,
    Course,
    Student,
    CourseMarks,
    Feedback,
    AuditLog,
)


class Command(BaseCommand):
    help = "Load realistic sample data for Student Portal"

    def handle(self, *args, **kwargs):

        demo_password = "DemoPass123!"

        # 1. Create Admin
        admin, created = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        admin.set_password(demo_password)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        UserProfile.objects.get_or_create(
            user=admin,
            defaults={"role": "admin"}
        )

        # 2. Create Trainers
        trainer_data = [
            ("trainer1", "trainer1@example.com"),
            ("trainer2", "trainer2@example.com"),
        ]

        trainers = []

        for username, email in trainer_data:
            trainer, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )

            trainer.set_password(demo_password)
            trainer.is_active = True
            trainer.save()

            UserProfile.objects.get_or_create(
                user=trainer,
                defaults={"role": "trainer"}
            )

            trainers.append(trainer)

        # 3. Create Departments
        department_names = [
            "Computer Science",
            "Information Technology",
            "Data Science",
        ]

        departments = []

        for name in department_names:
            department, created = Department.objects.get_or_create(
                name=name,
                defaults={"description": f"{name} Department"}
            )
            departments.append(department)

        # 4. Create Courses
        course_data = [
            ("Python Development", "PY101", "3 Months"),
            ("Django Development", "DJ101", "3 Months"),
            ("Web Development", "WEB101", "2 Months"),
            ("Data Science", "DS101", "4 Months"),
            ("SQL and Database", "SQL101", "2 Months"),
        ]

        courses = []

        for index, (name, code, duration) in enumerate(course_data):
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    "course_name": name,
                    "duration": duration,
                    "trainer": trainers[index % len(trainers)],
                    "active_status": True,
                }
            )
            courses.append(course)

        # 5. Create 20 Students
        student_names = [
            "Aarav Sharma", "Vivaan Verma", "Aditya Patel",
            "Arjun Singh", "Reyansh Gupta", "Ayaan Khan",
            "Krishna Joshi", "Ishaan Jain", "Rohan Mehta",
            "Rahul Yadav", "Priya Sharma", "Ananya Verma",
            "Aadhya Patel", "Diya Singh", "Saanvi Gupta",
            "Ira Khan", "Kavya Joshi", "Meera Jain",
            "Riya Mehta", "Sneha Yadav",
        ]

        students = []

        for index, name in enumerate(student_names, start=1):

            username = f"student{index:02d}"
            email = f"{username}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )

            user.set_password(demo_password)
            user.is_active = True
            user.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": "student"}
            )

            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    "name": name,
                    "email": email,
                    "age": 20 + (index % 8),
                    "department": departments[index % len(departments)],
                    "marks": 50 + (index % 50),
                    "joined_date": date.today() - timedelta(days=index * 5),
                    "is_active": True,
                }
            )

            # Assign courses
            assigned_courses = [
                courses[index % len(courses)],
                courses[(index + 1) % len(courses)],
            ]

            student.courses.add(*assigned_courses)
            students.append(student)

            # 6. Create Course Marks
            for course in assigned_courses:
                CourseMarks.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        "marks": 50 + (index * 2) % 51,
                        "updated_by": trainers[index % len(trainers)],
                        "reason": "Sample demo marks",
                    }
                )

        # 7. Create Feedback
        for index, student in enumerate(students):
            course = courses[index % len(courses)]
            trainer = course.trainer

            Feedback.objects.get_or_create(
                student=student,
                course=course,
                message="Good learning experience. Course content was helpful.",
                defaults={
                    "trainer": trainer,
                    "rating": (index % 5) + 1,
                    "is_visible": True,
                }
            )

        # 8. Create Audit Events
        for index, student in enumerate(students[:10]):
            AuditLog.objects.get_or_create(
                username=student.user.username,
                event="CREATE",
                details="Sample student account created.",
                defaults={
                    "user": student.user,
                    "affected_object": f"Student: {student.name}",
                }
            )

        AuditLog.objects.get_or_create(
            username=admin.username,
            event="LOGIN",
            details="Sample admin login event.",
            defaults={"user": admin}
        )

        AuditLog.objects.get_or_create(
            username=admin.username,
            event="UPDATE",
            details="Sample student record updated.",
            defaults={"user": admin}
        )

        self.stdout.write(
            self.style.SUCCESS("Sample data loaded successfully!")
        )

        self.stdout.write("DEMO LOGIN CREDENTIALS")
        self.stdout.write("----------------------")
        self.stdout.write("Admin:   demo_admin / DemoPass123!")
        self.stdout.write("Trainer: trainer1 / DemoPass123!")
        self.stdout.write("Trainer: trainer2 / DemoPass123!")
        self.stdout.write("Student: student01 / DemoPass123!")
