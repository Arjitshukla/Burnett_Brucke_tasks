from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Student,Department, Course, UserProfile,StudentProfile,AuditLog
from .forms import StudentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Avg,Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from functools import wraps
# from django.contrib.auth.views import PasswordChangeView


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                role = request.user.profile.role
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden("Access Denied")

            if role not in allowed_roles:
                return HttpResponseForbidden("You are not authorized!")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

# Create your views here.
def home(request):
    return render(request, "students/home.html")


def about(request):
    return render(request, "students/about.html")

@login_required
def student_list(request):
    # Get only the logged-in student's record
    role = request.user.profile.role

    if role == 'admin' or role == 'trainer':
        base_students = Student.objects.all()

    elif role == 'student':
        base_students = Student.objects.filter(user=request.user)

    else:
        return HttpResponseForbidden("Access Denied")

    students = base_students
    active_students = base_students.filter(is_active=True)
    total_students = base_students.count()

     # Get filter values from URL
    search = request.GET.get('search', '').strip()
    department_id = request.GET.get('department', '')
    course_id = request.GET.get('course', '')
    status = request.GET.get('status', '')
    result = request.GET.get('result', '')

     # Search by name, email, or course name
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

     # Department filter
    if department_id:
        students = students.filter(department_id=department_id)

    # Course filter
    if course_id:
        students = students.filter(courses__id=course_id)

    # Active status filter
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)

    # Pass / Fail filter
    if result == 'pass':
        students = students.filter(marks__gte=40)
    elif result == 'fail':
        students = students.filter(marks__lt=40)

    #pagination Implements
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'active_students': active_students,
        'total_count': total_students,
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'search': search,
        'selected_department': department_id,
        'selected_course': course_id,
        'selected_status': status,
        'selected_result': result,
    }
    return render (request, 'students/student_list.html', context)

@login_required
@role_required(['admin'])
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Student added successfully!"
            )
            return redirect("student_list")
    else:   
        form = StudentForm()

    return render( request, "students/add_student.html",{"form": form} )

@login_required

@login_required
def student_details(request, pk):

    role = request.user.profile.role

    if role in ['admin', 'trainer']:
        student = get_object_or_404(Student, pk=pk)

    elif role == 'student':
        student = get_object_or_404(
            Student,
            pk=pk,
            user=request.user
        )

    else:
        return HttpResponseForbidden("Access Denied")

    context = {
        'student': student
    }

    return render(request, "students/student_detail.html", context)

@login_required
@role_required(['admin'])
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("student_detail", pk=student.pk)

    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_form.html", {"form": form, "student": student})

@staff_member_required
@role_required(['admin'])
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect("student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {"student": student}
    )

# Authentication and Authorization

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "").strip()

        errors = {}
        non_field_errors = []

        # 1. Empty field validation
        if not username:
            errors['username'] = "Username is required."

        if not email:
            errors['email'] = "Email is required."

        if not password:
            errors['password'] = ["Password is required."]

        if not confirm_password:
            errors['confirm_password'] = "Confirm password is required."

        if errors:
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 2. Password matching validation
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 3. Duplicate username validation
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 4. Duplicate email validation
        if User.objects.filter(email__iexact=email).exists():
            errors['email'] = "Email already exists."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 5. Password strength validation
        try:
            validate_password(password,user=User(username=username, email=email))
        except ValidationError as error:
            errors['password'] = error.messages
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 6. Role validation
        if role not in ['student', 'trainer']:
            non_field_errors.append("Invalid role selected.")
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 7. Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=(role == 'student')
        )

        # 8. Create user profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "students/registration/register.html")


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        profile = UserProfile.objects.filter(
            user__username=username
        ).first()

        # Check whether account is locked
        if profile and profile.locked_until:

            if profile.locked_until > timezone.now():

                # Audit Login attempted
                AuditLog.objects.create(username=username,
                                        event="Login Blocked",
                                        details="Login attempted while account was locked.")
                messages.error(
                    request,
                    "Account temporarily locked. Please try again later."
                )
                return render(
                    request,
                    "students/registration/login.html"
                )

            else:
                profile.failed_login_attempts = 0
                profile.locked_until = None
                profile.save()

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Reset failed attempts after successful login
            if profile:
                profile.failed_login_attempts = 0
                profile.locked_until = None
                profile.save()

            # Audit successful login
            AuditLog.objects.create(
            username=username,
            event="Login Success",
            details="User logged in successfully."
)
            login(request, user)
            messages.success(request, "Login successful!")

            # Role-based redirect
            try:
                role = user.profile.role

                if role == 'admin':
                    return redirect('admin_dashboard')

                elif role == 'trainer':
                    return redirect('trainer_dashboard')

                elif role == 'student':
                    return redirect('student_dashboard')

                else:
                    messages.error(request, "Invalid user role.")
                    return redirect('login')

            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('login')

        else:

            # Audit failed login
            AuditLog.objects.create(
                username=username,
                event="Login Failed",
                details="Invalid username or password."
)
            if profile:
                profile.failed_login_attempts += 1

                if profile.failed_login_attempts >= 5:
                    profile.locked_until = (timezone.now() + timedelta(minutes=15))

                    AuditLog.objects.create(
                                username=username,
                                event="Account Locked",
                                details="Account locked for 15 minutes.")
                    
                    messages.error(
                        request,
                        "Too many failed attempts. Account locked for 15 minutes."
                    )
                else:
                    messages.error(
                        request,
                        f"Invalid credentials. Attempts remaining: {5 - profile.failed_login_attempts}"
                    )

                profile.save()

            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "students/registration/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def dashboard(request):

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        is_active=True
    ).count()

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    average_marks = Student.objects.aggregate(
        Avg("marks")
    )["marks__avg"]

    highest_student = Student.objects.order_by(
        "-marks"
    ).first()
    recent_students = Student.objects.order_by(
        "-joined_date"
    )[:5]
    context = {
        "total_students": total_students,
        "active_students": active_students,
        "total_departments": total_departments,
        "total_courses": total_courses,
        "average_marks": average_marks,
        "highest_student": highest_student,
        "recent_students": recent_students,
    }

    return render(
        request,
        "students/dashboard.html",
        context
    )

# Admin_dashboard
@login_required
@role_required(['admin'])
def admin_dashboard(request):

    context = {
        'total_users': User.objects.count(),
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),

        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_students': Student.objects.order_by('-id')[:5],
        'recent_courses': Course.objects.order_by('-id')[:5],
    }

    return render(
        request,
        'students/dashboards/admin_dashboard.html',
        context
    )


# trainer dashboard
@login_required
@role_required(['trainer'])
def trainer_dashboard(request):

    courses = Course.objects.filter(
        trainer=request.user
    )

    students = Student.objects.filter(
        courses__trainer=request.user
    ).distinct()

    context = {
        'courses': courses,
        'students': students,
        'total_courses': courses.count(),
        'total_students': students.count(),
    }

    return render(
        request,
        'students/dashboards/trainer_dashboard.html',
        context
    )

# Student dashboard
@login_required
@role_required(['student'])
def student_dashboard(request):

    try:
        student = request.user.student_record
    except Student.DoesNotExist:
        student = None

    profile_completion = 0

    if student:
        try:
            profile = student.profile
        except StudentProfile.DoesNotExist:
            profile = None

        fields = [
            student.name,
            student.email,
            student.age,
            student.department,
            profile.phone if profile else None,
            profile.address if profile else None,
            profile.date_of_birth if profile else None,
        ]

        completed_fields = sum(
            1 for field in fields if field
        )

        profile_completion = round(
            (completed_fields / len(fields)) * 100
        )

    return render(
        request,
        'students/dashboards/student_dashboard.html',
        {
            'student': student,
            'profile_completion': profile_completion,
        }
    )