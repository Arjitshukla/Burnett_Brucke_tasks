from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from ..models import Student,Department, Course,StudentProfile,Feedback
from ..forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg,Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from ..utils import create_audit_log
from ..decorators import role_required



# # Create your views here.
def home(request):
    return render(request, "students/home.html")


def about(request):
    return render(request, "students/about.html")

# STUDENT LIST VIEW
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
    # optimise Query

    base_students = base_students.select_related(
    'department',
    'user'
).prefetch_related('courses')   
    
    students = base_students
    active_students = base_students.filter(is_active=True).order_by('-id')
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
    students = students.order_by('-id')
    paginator = Paginator(students, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'active_students': active_students,
        'total_count': total_students,
        'departments': Department.objects.values('id', 'name'),
        'courses': Course.objects.values('id', 'course_name','code'),
        'search': search,
        'selected_department': department_id,
        'selected_course': course_id,
        'selected_status': status,
        'selected_result': result,
        'total_active_student':total_active_student
    }
    return render (request, 'students/student_list.html', context)


# ADD STUDENT VIEW
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


# STUDENTS DETAILS VIEW
@login_required 
@role_required(['admin','student'])
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


# EDIT STUDENT VIEWS
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


# STUDENT DELETE VIEW
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

# STUDENT DASHBOARD 
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