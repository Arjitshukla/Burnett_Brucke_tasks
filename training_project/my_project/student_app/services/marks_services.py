from ..models import MarksUpdateHistory
from ..utils import create_audit_log


def update_student_course_marks(student, course, form, user, request, previous_marks):
    """
    Update student course marks and maintain marks history
    and audit log.
    """

    course_marks = form.save(commit=False)

    previous_marks = (
        course_marks.marks if course_marks.pk else 0
    )

    course_marks.student = student
    course_marks.course = course
    course_marks.updated_by = user
    course_marks.save()

    MarksUpdateHistory.objects.create(
        student=student,
        course=course,
        previous_marks=previous_marks,
        new_marks=course_marks.marks,
        updated_by=user,
        reason=course_marks.reason
    )

    create_audit_log(
        request,
        "MARKS_UPDATE",
        f"Marks changed from {previous_marks} to {course_marks.marks}.",
        affected_object=f"{student.name} - {course.course_name}",
        user=user
    )

    return course_marks