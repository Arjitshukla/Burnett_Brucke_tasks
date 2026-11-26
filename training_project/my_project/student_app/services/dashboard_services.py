
def get_trainer_student_rows(students, trainer):
    """
    Prepare student-wise assigned courses and marks data
    for the trainer dashboard.
    """

    student_rows = []

    for student in students:

        assigned_courses = [
            course for course in student.courses.all()
            if course.trainer_id == trainer.id
        ]

        course_rows = []

        marks_records = {
            record.course_id: record
            for record in student.course_marks.all()
        }

        for course in assigned_courses:

            marks_record = marks_records.get(course.id)

            course_rows.append({
                'course': course,
                'marks_record': marks_record
            })

        student_rows.append({
            'student': student,
            'course_rows': course_rows
        })

    return student_rows
