# Service Layer Documentation

## 1. Overview

The service layer separates business logic from Django views. It makes the code more organized, reusable, and easier to maintain.

## 2. Extracted Services

### Dashboard Service
- File: `dashboard_services.py`
- Function: `get_trainer_student_rows()`
- Prepares student-wise course and marks data for the trainer dashboard.

### Marks Service
- File: `marks_services.py`
- Function: `update_student_course_marks()`
- Updates student marks, creates marks history, and generates audit logs.

### Feedback Service
- File: `feedback_services.py`
- Functions:
  - `create_student_feedback()`
  - `update_student_feedback()`
- Handles feedback creation, updating, and audit logging.

## 3. View Responsibilities

Views are now mainly responsible for:
- Handling HTTP requests.
- Validating submitted forms.
- Calling service functions.
- Returning responses such as render or redirect.

Business logic is handled separately in service modules.

## 4. Reusability in APIs

The extracted service functions can also be called from Django REST Framework API views.

For example, an API view can call `update_student_course_marks()` instead of implementing marks updating, history creation, and audit logging again.

This avoids duplicate business logic between web views and API views.

The service layer makes future API development easier because the same business operations can be reused across different interfaces.

## 5. Benefits

- Reduces code duplication.
- Improves maintainability.
- Keeps views simple and focused.
- Makes business logic reusable.
- Simplifies future API integration.