from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from ..models import Student,Course,Feedback,CourseMarks,MarksUpdateHistory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ..utils import create_audit_log
from ..decorators import role_required
from ..forms import FeedbackForm,CourseMarksForm
# servics 
from ..services.dashboard_services import get_trainer_student_rows
from ..services.marks_services import update_student_course_marks
from ..services.feedback_services import create_student_feedback,update_student_feedback



# Trainer Dashboard
@login_required
@role_required(['trainer'])
def trainer_dashboard(request):

    # Get trainer's assigned courses
    courses = Course.objects.filter(
        trainer=request.user
    )

    # Get students assigned to trainer's courses
    # Prefetch courses, marks records and updated_by users
    students = Student.objects.filter(
        courses__trainer=request.user
    ).distinct().prefetch_related(
        'courses',
        'course_marks__updated_by'
    )
    # Prepare student and course-wise marks data using service
    student_rows = get_trainer_student_rows(students, request.user)

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

            if not trainer_courses.filter(id=form.cleaned_data['course'].id).exists():
                return HttpResponseForbidden("Invalid course selection.")
            # feedback_services
            create_student_feedback(
                student,
                request.user,
                form,
                request
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

    previous_marks = course_marks.marks if course_marks else 0
    if request.method == 'POST':
        form = CourseMarksForm(
            request.POST,
            instance=course_marks
        )

        if form.is_valid():
            # marks_services
            update_student_course_marks(
                student,
                course,
                form,
                request.user,
                request,
                previous_marks
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
            # feedback_services
            update_student_feedback(
                feedback,
                form,
                request,
                request.user
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
