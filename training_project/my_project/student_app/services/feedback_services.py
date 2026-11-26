from ..utils import create_audit_log


def create_student_feedback(student, trainer, form, request):
    """
    Create feedback for a student and generate an audit log.
    """

    feedback = form.save(commit=False)
    feedback.student = student
    feedback.trainer = trainer
    feedback.save()

    create_audit_log(
        request,
        "FEEDBACK_CREATE",
        "Trainer created feedback for student.",
        affected_object=f"Feedback: {student.name}",
        user=trainer
    )

    return feedback


def update_student_feedback(feedback, form, request, user):
    """
    Update existing feedback and generate an audit log.
    """

    updated_feedback = form.save()

    create_audit_log(
        request,
        "UPDATE",
        "Trainer updated feedback.",
        affected_object=f"Feedback: {feedback.student.name}",
        user=user
    )

    return updated_feedback