from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration = models.CharField(max_length=50)
    active_status = models.BooleanField(default=True)
    trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_courses'
    )
    def __str__(self):
        return f"{self.course_name} ({self.code})"
    
    
class Student(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='student_record'
)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students",
        null=True, blank= True
    )
    courses = models.ManyToManyField(
    Course,
    related_name="students",
    blank=True
)
    marks = models.FloatField()
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class CourseMarks(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='course_marks'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='student_marks'
    )
    marks = models.FloatField(default=0)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    reason = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"


class MarksUpdateHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    previous_marks = models.FloatField()
    new_marks = models.FloatField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    updated_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"

    
    
class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.student.name} - Profile"

# usermodel
class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    # to prevent multiple password attempt
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# AuditLog model

class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('FAILED', 'Failed Login'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('MARKS_UPDATE', 'Marks Update'),
        ('FEEDBACK_CREATE', 'Feedback Created'),
        ('ACCOUNT_STATUS_CHANGE', 'Account Status Changed'),
    ]

    username = models.CharField(max_length=150)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    event = models.CharField(
        max_length=100,
        choices=ACTION_CHOICES
    )

    affected_object = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    details = models.TextField(blank=True, null=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.event}"


# feedback model
class Feedback(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_feedbacks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    message = models.TextField()
    rating = models.PositiveIntegerField(
    default=5,
    choices=[(i, i) for i in range(1, 6)]
)
    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"   