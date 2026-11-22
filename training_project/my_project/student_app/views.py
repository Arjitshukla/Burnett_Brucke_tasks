from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Student,Department, Course, UserProfile,StudentProfile,AuditLog,Feedback,CourseMarks, MarksUpdateHistory
from .forms import StudentForm,FeedbackForm,CourseMarksForm
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

# resuable Aduitlog function
def create_audit_log(request, event, details="", affected_object="", user=None, username=None):
    actor = user if user is not None else (
        request.user if request.user.is_authenticated else None
    )
    AuditLog.objects.create(
        username=username or (actor.username if actor else "Anonymous"),
        user=actor,
        event=event,
        affected_object=affected_object,
        details=details,
        ip_address=request.META.get('REMOTE_ADDR')
    )




# role custum decorator
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
    active_students = base_students.filter(is_active=True).order_by('-id')[:6]
    total_active_student = active_students.count()
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
    page_obj = paginator.get_page(request.GET.get('page'))

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
        'total_active_student':total_active_student
    }
    return render (request, 'students/student_list.html', context)

@login_required
@role_required(['admin'])
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()

            create_audit_log(
                request,
                "CREATE",
                "New student record created.",
                affected_object=f"Student: {student}",
                user=request.user
            )
            messages.success(
                request,
                "Student added successfully!"
            )
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(request,"students/add_student.html",{"form": form})

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
        old_marks = student.marks
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            updated_student = form.save()

            if old_marks != updated_student.marks:
                create_audit_log(
                    request,
                    "MARKS_UPDATE",
                    f"Marks changed from {old_marks} to {updated_student.marks}",
                    affected_object=f"Student: {updated_student}",
                    user=request.user
                )
            else:
                create_audit_log(
                    request,
                    "UPDATE",
                    "Student information updated.",
                    affected_object=f"Student: {updated_student}",
                    user=request.user
                )

            messages.success(request, "Student updated successfully!")
            return redirect("student_detail", pk=student.pk)

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {"form": form, "student": student}
    )



@staff_member_required
@role_required(['admin'])
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":

        student_name = str(student)

        create_audit_log(
            request,
            "DELETE",
            "Student record deleted.",
            affected_object=f"Student: {student_name}",
            user=request.user
        )

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
                create_audit_log(
                    request,
                    "Login Blocked",
                    "Login attempted while account was locked.",
                    user=profile.user,
                    username=username
                )
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
            create_audit_log(
                    request,
                    "LOGIN",
                    "User logged in successfully.",
                    user=profile.user,
                    username=username
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
            create_audit_log(
                    request,
                    "FAILED",
                    "Invalid username or password.",
                    user=profile.user if profile else None,
                    username=username
                )
            if profile:
                profile.failed_login_attempts += 1

                if profile.failed_login_attempts >= 5:
                    profile.locked_until = (timezone.now() + timedelta(minutes=15))

                    # AduitLog for Account locked
                    create_audit_log(
                    request,
                    "Account Locked",
                    "Account locked for 15 minutes.",
                    user=profile.user,
                    username=username
                )
                    
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
    if request.user.is_authenticated:

        create_audit_log(
            request,
            "LOGOUT",
            "User logged out successfully.",
            user=request.user
        )

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

@login_required
@role_required(['admin'])
def all_feedback_view(request):
    feedbacks = Feedback.objects.select_related(
        'student', 'trainer', 'course'
    ).order_by('-created_at')

    return render(
        request,    
        'students/all_feedback.html',
        {'feedbacks': feedbacks}
    )

@login_required
@role_required(['admin'])
def toggle_feedback_visibility(request, feedback_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_visible = not feedback.is_visible
    feedback.save()

    messages.success(request, "Feedback visibility updated.")
    return redirect('all_feedback')


@login_required
@role_required(['admin'])
def toggle_user_status(request, user_id):

    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    target_user = get_object_or_404(User, id=user_id)

    old_status = target_user.is_active

    target_user.is_active = not target_user.is_active
    target_user.save()

    new_status = target_user.is_active

    create_audit_log(
        request,
        "ACCOUNT_STATUS_CHANGE",
        f"Account status changed from {'Active' if old_status else 'Inactive'} to {'Active' if new_status else 'Inactive'}.",
        affected_object=f"User: {target_user.username}",
        user=request.user
    )

    messages.success(
        request,
        f"{target_user.username}'s account status updated successfully."
    )

    return redirect('admin_dashboard')


@login_required
@role_required(['admin'])
def audit_logs_view(request):

    logs = AuditLog.objects.all().order_by('-timestamp')

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        logs = logs.filter(
            Q(username__icontains=search) |
            Q(affected_object__icontains=search) |
            Q(details__icontains=search)
        )

    # Event filter
    event = request.GET.get('event', '')
    if event:
        logs = logs.filter(event=event)

    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)

    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)

    # Pagination
    paginator = Paginator(logs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'events': AuditLog.ACTION_CHOICES,
        'search': search,
        'selected_event': event,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(
        request,
        'students/audit_logs.html',
        context
    )




# trainer dashboard

# Trainer Dashboar
@login_required
@role_required(['trainer'])
def trainer_dashboard(request):

    # Get trainer's assigned courses
    courses = Course.objects.filter(
        trainer=request.user
    )

    # Get students assigned to trainer's courses
    students = Student.objects.filter(
        courses__trainer=request.user
    ).distinct()

    # Prepare student and course-wise marks data
    student_rows = []

    for student in students:

        assigned_courses = student.courses.filter(
            trainer=request.user
        )

        course_rows = []

        for course in assigned_courses:

            marks_record = CourseMarks.objects.filter(
                student=student,
                course=course
            ).select_related('updated_by').first()

            course_rows.append({
                'course': course,
                'marks_record': marks_record
            })

        student_rows.append({
            'student': student,
            'course_rows': course_rows
        })

    # Get trainer's feedback
    feedbacks = Feedback.objects.filter(
        trainer=request.user
    ).select_related(
        'student',
        'course'
    ).order_by('-created_at')

    # Dashboard context
    context = {
        'courses': courses,
        'students': students,
        'total_courses': courses.count(),
        'total_students': students.count(),
        'feedbacks': feedbacks,
        'student_rows': student_rows,
    }

    return render(
        request,
        'students/dashboards/trainer_dashboard.html',
        context
    )



# for give feedback to perticular students
@login_required
@role_required(['trainer'])
def give_feedback(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    # Get courses assigned to this trainer
    trainer_courses = Course.objects.filter(
        trainer=request.user,
        students=student
    )

    if not trainer_courses.exists():
        return HttpResponseForbidden(
            "You are not allowed to give feedback to this student."
        )

    if request.method == 'POST':

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save(commit=False)

            # Verify selected course belongs to this trainer and student
            if not trainer_courses.filter(id=feedback.course_id).exists():
                return HttpResponseForbidden("Invalid course selection.")

            feedback.student = student
            feedback.trainer = request.user
            feedback.save()

            create_audit_log(
                request,
                "FEEDBACK_CREATE",
                "Trainer created feedback for student.",
                affected_object=f"Feedback: {student.name}",
                user=request.user
            )

            messages.success(request, "Feedback submitted successfully!")
            return redirect('trainer_dashboard')

    else:
        form = FeedbackForm()

    # Show only courses assigned to this trainer and student
    form.fields['course'].queryset = trainer_courses

    return render(
        request,
        'students/give_feedback.html',
        {
            'form': form,
            'student': student
        }
    )



# for editing feedback by trainer
@login_required
@role_required(['trainer'])
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        trainer=request.user
    )

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)

        if form.is_valid():
            form.save()

            create_audit_log(
                request,
                "UPDATE",
                "Trainer updated feedback.",
                affected_object=f"Feedback: {feedback.student.name}",
                user=request.user
            )

            messages.success(request, "Feedback updated successfully!")
            return redirect('trainer_dashboard')
    else:
        form = FeedbackForm(instance=feedback)

    return render(
        request,
        'students/edit_feedback.html',
        {'form': form, 'feedback': feedback}
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
    feedbacks = Feedback.objects.none()

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

        # Get feedback received by this student only
        feedbacks = Feedback.objects.filter(
        student=student,
        is_visible=True
    ).select_related('trainer', 'course').order_by('-created_at')

    return render(
        request,
        'students/dashboards/student_dashboard.html',
        {
            'student': student,
            'profile_completion': profile_completion,
            'feedbacks': feedbacks,
        }
    )


# Marks History View
@login_required
@role_required(['trainer'])
def update_course_marks(request, student_id, course_id):

    student = get_object_or_404(
        Student,
        id=student_id,
        courses__id=course_id,
        courses__trainer=request.user
    )

    course = get_object_or_404(
        Course,
        id=course_id,
        trainer=request.user
    )

    course_marks = CourseMarks.objects.filter(
        student=student,
        course=course
    ).first()

    if request.method == 'POST':
        form = CourseMarksForm(
            request.POST,
            instance=course_marks
        )

        if form.is_valid():
            previous_marks = (
                course_marks.marks if course_marks else 0
            )

            marks_record = form.save(commit=False)
            marks_record.student = student
            marks_record.course = course
            marks_record.updated_by = request.user
            marks_record.save()

            MarksUpdateHistory.objects.create(
                student=student,
                course=course,
                previous_marks=previous_marks,
                new_marks=marks_record.marks,
                updated_by=request.user,
                reason=marks_record.reason
            )

            create_audit_log(
                request,
                "MARKS_UPDATE",
                f"Marks changed from {previous_marks} to {marks_record.marks}.",
                affected_object=f"{student.name} - {course.course_name}",
                user=request.user
            )

            messages.success(request, "Marks updated successfully!")
            return redirect('trainer_dashboard')

    else:
        form = CourseMarksForm(instance=course_marks)

    return render(
        request,
        'students/update_course_marks.html',
        {
            'form': form,
            'student': student,
            'course': course
        }
    )


# @login_required
@role_required(['admin'])
def marks_history_view(request):

    history = MarksUpdateHistory.objects.select_related(
        'student',
        'course',
        'updated_by'
    ).order_by('-updated_at')

    context = {
        'history': history
    }

    return render(
        request,
        'students/marks_history.html',
        context
    )
