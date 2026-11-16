from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Student,Department, Course
from .forms import StudentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Avg,Q


# Create your views here.
def home(request):
    return render(request, "students/home.html")


def about(request):
    return render(request, "students/about.html")

@login_required
def student_list(request):
    students = Student.objects.all()
    active_students = Student.objects.filter(is_active=True)
    total_students = Student.objects.count()

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


    context = {
        'students': students,
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
def student_details(request,pk):
    student = get_object_or_404(Student,pk=pk)
    context = {'student':student}
    return render(
        request,
        "students/student_detail.html",
        context
    )

@login_required
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

        # 1. Empty field validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        # 2. Password matching validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # 3. Duplicate username validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # 4. Password strength validation
        try:
            validate_password(password)
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)
            return redirect("register")

        # 5. Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "students/register.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("/students/")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "students/login.html")


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
