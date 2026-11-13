from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm


# Create your views here.
def home(request):
    return render(request, "students/home.html")


def about(request):
    return render(request, "students/about.html")


def student_list(request):
    students = Student.objects.all()
    active_students = Student.objects.filter(is_active=True)
    total_students = Student.objects.count()
    context = {'students': students,'active_students':active_students,'total_count':total_students}
    return render (request, 'students/student_list.html', context)

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


def student_details(request,pk):
    student = get_object_or_404(Student,pk=pk)
    context = {'student':student}
    return render(
        request,
        "students/student_detail.html",
        context
    )

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