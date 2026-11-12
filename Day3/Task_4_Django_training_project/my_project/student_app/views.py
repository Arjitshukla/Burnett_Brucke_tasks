from django.shortcuts import render
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.shortcuts import redirect

# Create your views here.

def student_detail(request):
    students = Student.objects.all()
    active_students = Student.objects.filter(is_active=True)
    total_students = Student.objects.count()
    context = {'students': students,'active_students':active_students,'total_count':total_students}
    return render (request, 'students/student_detail.html', context)

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Student added successfully!"
            )
            return redirect("student_detail")
    else:   
        form = StudentForm()

    return render( request, "students/add_student.html",{"form": form} )