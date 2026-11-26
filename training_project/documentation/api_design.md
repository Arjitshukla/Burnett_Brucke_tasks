# Student Training Portal – API Design Document

## 1. Introduction

This document defines the REST API design for the Student Training Portal.

The API will allow authorized users to manage student records, courses, enrollments, marks, and feedback.

The API will follow REST principles and use JSON for request and response data.

### Base URL

```text
/api/
```

### Authentication

The API will use authentication to identify users and role-based permissions to control access.

Supported roles:

- Admin
- Trainer
- Student

For the API implementation, Django REST Framework with Token Authentication can be used.

Unauthenticated requests will receive `401 Unauthorized`, and users without sufficient permissions will receive `403 Forbidden`.

---

## 2. API Resources

The following resources will be exposed through the API:

| Resource | Description |
|---|---|
| Students | Manage student records |
| Courses | Retrieve and manage course information |
| Enrollments | Manage student-course relationships |
| Marks | Manage course-wise student marks |
| Feedback | Create, retrieve, update and manage feedback |

**Note:** The project does not have a separate Enrollment model. Enrollment is implemented using the ManyToMany relationship between `Student` and `Course`.

---

## 3. Student APIs

Student APIs will manage student records, including creation, retrieval, updating, deletion, searching and filtering.

### 3.1 List Students

**Endpoint:** `GET /api/students/`

**Permissions:**
- Admin: Can view all students.
- Trainer: Can view students assigned to their courses.
- Student: Can view only their own record.

**Query Parameters:**

| Parameter | Description |
|---|---|
| search | Search by name, email or course name |
| department | Filter by department ID |
| course | Filter by course ID |
| status | Filter active or inactive students |
| result | Filter pass or fail students |
| page | Pagination page number |

**Response – 200 OK**

```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Rahul Sharma",
      "email": "rahul@example.com",
      "age": 22,
      "department": 1,
      "marks": 85,
      "is_active": true
    },
    {
      "id": 2,
      "name": "Aman Verma",
      "email": "aman@example.com",
      "age": 23,
      "department": 2,
      "marks": 65,
      "is_active": true
    }
  ]
}
```

### 3.2 Create Student

**Endpoint:** `POST /api/students/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "age": 22,
  "department": 1,
  "marks": 85,
  "joined_date": "2026-11-26",
  "is_active": true
}
```

**Validation:**
- Name and email are required.
- Age must be between 16 and 60.
- Department must reference a valid department.
- Marks must be within the valid range defined for student marks.
- Email must have a valid format.

**Response – 201 Created**

```json
{
  "message": "Student created successfully.",
  "student_id": 1
}
```

### 3.3 Retrieve Student Details

**Endpoint:** `GET /api/students/{id}/`

**Permissions:**
- Admin: Any student.
- Trainer: Students assigned to their courses.
- Student: Own record only.

**Response – 200 OK**

```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "age": 22,
  "department": 1,
  "marks": 85,
  "joined_date": "2026-11-26",
  "is_active": true
}
```

### 3.4 Update Student

**Endpoint:** `PATCH /api/students/{id}/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "name": "Rahul Kumar",
  "age": 23,
  "marks": 90
}
```

**Response – 200 OK**

```json
{
  "message": "Student updated successfully."
}
```

The API will create an audit log when student information or marks are updated.

### 3.5 Delete Student

**Endpoint:** `DELETE /api/students/{id}/`

**Permission:** Admin only.

**Response – 204 No Content**

The student record will be deleted. Related records will follow the deletion behavior defined by the Django model relationships.

---

## 4. Course APIs

Course APIs will provide access to course information and course management.

### 4.1 List Courses

**Endpoint:** `GET /api/courses/`

**Permissions:**
- Admin: All courses.
- Trainer: Assigned courses.
- Student: Courses available or assigned to the student.

**Response – 200 OK**

```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "course_name": "Python Development",
      "code": "PY101",
      "duration": "3 Months",
      "active_status": true,
      "trainer": 5
    },
    {
      "id": 2,
      "course_name": "Django Development",
      "code": "DJ101",
      "duration": "2 Months",
      "active_status": true,
      "trainer": 6
    }
  ]
}
```

### 4.2 Retrieve Course Details

**Endpoint:** `GET /api/courses/{id}/`

**Permissions:** Admin, assigned trainer and eligible student.

**Response – 200 OK**

```json
{
  "id": 1,
  "course_name": "Python Development",
  "code": "PY101",
  "duration": "3 Months",
  "active_status": true,
  "trainer": 5
}
```

### 4.3 Create Course

**Endpoint:** `POST /api/courses/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "course_name": "Python Development",
  "code": "PY101",
  "duration": "3 Months",
  "active_status": true,
  "trainer": 5
}
```

**Response – 201 Created**

```json
{
  "message": "Course created successfully.",
  "course_id": 1
}
```

### 4.4 Update Course

**Endpoint:** `PATCH /api/courses/{id}/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "duration": "4 Months",
  "active_status": false
}
```

**Response – 200 OK**

```json
{
  "message": "Course updated successfully."
}
```

### 4.5 Delete Course

**Endpoint:** `DELETE /api/courses/{id}/`

**Permission:** Admin only.

**Response – 204 No Content**

The course will be deleted according to the configured model relationships.

---

## 5. Enrollment APIs

Enrollment represents the relationship between students and courses.

The project uses the `Student.courses` ManyToMany field instead of a separate Enrollment model.

### 5.1 Get Student Enrollments

**Endpoint:** `GET /api/students/{student_id}/courses/`

**Permissions:**
- Admin: All students.
- Trainer: Students assigned to their courses.
- Student: Own enrollments only.

**Response – 200 OK**

```json
{
  "student_id": 1,
  "courses": [
    {
      "id": 1,
      "course_name": "Python Development",
      "code": "PY101"
    },
    {
      "id": 2,
      "course_name": "Django Development",
      "code": "DJ101"
    }
  ]
}
```

### 5.2 Enroll Student in Course

**Endpoint:** `POST /api/students/{student_id}/courses/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "course_id": 1
}
```

**Response – 201 Created**

```json
{
  "message": "Student enrolled successfully."
}
```

**Validation:**
- Student must exist.
- Course must exist.
- Duplicate enrollment should not be created.
- Only active courses should be allowed for new enrollment.

### 5.3 Remove Student Enrollment

**Endpoint:** `DELETE /api/students/{student_id}/courses/{course_id}/`

**Permission:** Admin only.

**Response – 204 No Content**

The student will be removed from the selected course without deleting the student or course itself.

---

## 6. Marks APIs

Marks APIs will manage course-wise student marks.

The project uses two models:

- `CourseMarks`: Stores current marks for a student in a course.
- `MarksUpdateHistory`: Stores previous and updated marks, the user who updated them, timestamp and reason.

### 6.1 Get Student Marks

**Endpoint:** `GET /api/students/{student_id}/marks/`

**Permissions:**
- Admin: All student marks.
- Trainer: Marks for students in their assigned courses.
- Student: Own marks only.

**Response – 200 OK**

```json
{
  "student_id": 1,
  "marks": [
    {
      "course_id": 1,
      "course_name": "Python Development",
      "marks": 85,
      "reason": "Monthly assessment",
      "updated_at": "2026-11-26T10:30:00Z"
    }
  ]
}
```

### 6.2 Add or Update Course Marks

**Endpoint:** `POST /api/students/{student_id}/courses/{course_id}/marks/`

**Permission:** Trainer assigned to the course.

**Request Body:**

```json
{
  "marks": 85,
  "reason": "Monthly assessment"
}
```

**Response – 200 OK**

```json
{
  "message": "Marks updated successfully.",
  "student_id": 1,
  "course_id": 1,
  "marks": 85
}
```

If no marks record exists, the API will create one. Otherwise, it will update the existing record.

**Validation:**
- Marks must be between 0 and 100.
- Student must be enrolled in the course.
- Trainer must be assigned to that course.
- A marks update should create a corresponding history record.
- The authenticated trainer should be recorded as `updated_by`.

### 6.3 Get Marks Update History

**Endpoint:** `GET /api/students/{student_id}/marks/history/`

**Permissions:**
- Admin: All marks history.
- Trainer: History for students in their assigned courses.
- Student: Own marks history.

**Response – 200 OK**

```json
{
  "student_id": 1,
  "history": [
    {
      "course_id": 1,
      "previous_marks": 75,
      "new_marks": 85,
      "updated_by": "trainer1",
      "reason": "Monthly assessment",
      "updated_at": "2026-11-26T10:30:00Z"
    }
  ]
}
```

---

## 7. Feedback APIs

Feedback APIs will manage feedback submitted by trainers for students.

### 7.1 List Feedback

**Endpoint:** `GET /api/feedback/`

**Permissions:**
- Admin: All feedback.
- Trainer: Feedback created by that trainer.
- Student: Own visible feedback only.

**Response – 200 OK**

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "student": 1,
      "trainer": 5,
      "course": 1,
      "message": "Good performance.",
      "rating": 5,
      "is_visible": true,
      "created_at": "2026-11-26T10:30:00Z"
    }
  ]
}
```

### 7.2 Create Feedback

**Endpoint:** `POST /api/students/{student_id}/feedback/`

**Permission:** Trainer assigned to the student's course.

**Request Body:**

```json
{
  "course": 1,
  "rating": 5,
  "message": "Good performance."
}
```

**Response – 201 Created**

```json
{
  "message": "Feedback submitted successfully."
}
```

**Validation:**
- Student must exist.
- Course must be assigned to the trainer.
- Student must be enrolled in the selected course.
- Rating must be between 1 and 5.
- Feedback message must be valid.

### 7.3 Update Feedback

**Endpoint:** `PATCH /api/feedback/{feedback_id}/`

**Permission:** The trainer who created the feedback.

**Request Body:**

```json
{
  "rating": 4,
  "message": "Performance has improved."
}
```

**Response – 200 OK**

```json
{
  "message": "Feedback updated successfully."
}
```

### 7.4 Toggle Feedback Visibility

**Endpoint:** `PATCH /api/feedback/{feedback_id}/visibility/`

**Permission:** Admin only.

**Request Body:**

```json
{
  "is_visible": false
}
```

**Response – 200 OK**

```json
{
  "message": "Feedback visibility updated successfully.",
  "is_visible": false
}
```

---

## 8. Permissions Summary

| Operation | Admin | Trainer | Student |
|---|---|---|---|
| View all students | Yes | Assigned students | No |
| View own student record | Yes | Yes, if assigned | Yes |
| Create student | Yes | No | No |
| Update student | Yes | No | No |
| Delete student | Yes | No | No |
| View courses | All | Assigned | Enrolled |
| Create/update/delete course | Yes | No | No |
| Manage enrollments | Yes | No | No |
| View marks | All | Assigned students | Own marks |
| Add/update marks | No | Assigned courses | No |
| View marks history | All | Assigned students | Own history |
| View feedback | All | Own feedback | Own visible feedback |
| Create feedback | No | Assigned students | No |
| Edit feedback | No | Own feedback | No |
| Toggle feedback visibility | Yes | No | No |

---

## 9. HTTP Status Codes

The API will use standard HTTP status codes.

| Status Code | Description | Usage |
|---|---|---|
| 200 OK | Request successful | Retrieve or update resources |
| 201 Created | Resource created | Student, course, enrollment or feedback creation |
| 204 No Content | Resource deleted | Successful DELETE operation |
| 400 Bad Request | Invalid request data | Validation errors or malformed input |
| 401 Unauthorized | Authentication required | Missing or invalid authentication |
| 403 Forbidden | Permission denied | User does not have the required role |
| 404 Not Found | Resource not found | Invalid student, course or feedback ID |
| 405 Method Not Allowed | Unsupported HTTP method | Invalid method for an endpoint |
| 409 Conflict | Resource conflict | Duplicate enrollment or unique course code |
| 500 Internal Server Error | Server error | Unexpected application failure |

---

## 10. Validation and Security

The API will follow the validation and security rules already established in the project.

### Student Validation
- Age must be between 16 and 60.
- Email must be valid.
- Department must exist.
- Only authorized administrators can create, update or delete student records.

### Course Validation
- Course code must be unique.
- Course name and duration must be valid.
- Assigned trainer must reference a valid user.

### Marks Validation
- Marks must be between 0 and 100.
- Trainers can update marks only for their assigned courses.
- Previous and updated marks must be recorded in marks history.

### Feedback Validation
- Rating must be between 1 and 5.
- Trainers can provide feedback only for students enrolled in their assigned courses.
- Trainers can edit only their own feedback.
- Students can access only visible feedback belonging to them.

### Authentication Security
- Passwords must be validated using Django password validators.
- Login attempts should follow the existing account-locking policy.
- After five failed login attempts, the account is locked for 15 minutes.
- Protected endpoints must require authentication.
- Role-based permissions must be checked on every protected operation.

### Audit Logging
Important operations should be recorded using the existing `create_audit_log()` utility.

Events include:
- Student creation, update and deletion.
- Marks updates.
- Account status changes.
- Authentication events.

Audit logs should include the acting user, event, affected object, details, IP address and timestamp where available.

---

## 11. API Implementation Structure

The proposed API can be organized separately from the existing web views.

```text
student_app/
│
├── models.py
├── serializers.py
├── permissions.py
│
├── api/
│   ├── __init__.py
│   ├── urls.py
│   │
│   └── views/
│       ├── __init__.py
│       ├── student_views.py
│       ├── course_views.py
│       ├── enrollment_views.py
│       ├── marks_views.py
│       └── feedback_views.py
│
├── services/
│   ├── dashboard_services.py
│   ├── marks_services.py
│   └── feedback_services.py
│
├── decorators.py
├── utils.py
└── forms.py
```

Existing service functions for marks and feedback can be reused where appropriate, with API-specific serializers and validation.

---

## 12. Conclusion

This API design provides a structured way to expose the Student Training Portal functionality through REST endpoints.

It covers student management, course management, student enrollments, course-wise marks, marks history and feedback management.

The API will maintain role-based access control, input validation, authentication security and audit logging.

The design is based on the existing Django models and business logic, while defining additional API endpoints required to expose these features through a REST interface.