
# Student Management System

A Django-based Student Management System that allows users to manage student records, view student details, and add new students through a web form.

## 1. Project Setup

### Clone the Repository

```bash
git clone <repository-url>
cd day3/my_project
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Database Migrations

Run the following commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3. Create Superuser

Create an admin account to access the Django admin panel.

```bash
python manage.py createsuperuser
```
## 4. Run Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## 5. Created URLs

| URL | Description |
|---|---|
| `http://127.0.0.1:8000//admin/` | Django Admin Panel |
| `http://127.0.0.1:8000/` | Display all student records |
| `http://127.0.0.1:8000/add_student/` | Add a new student |

## 6. Tasks Completed

### Task 4: Django Models and Admin Panel

- Created Student model with Name, Email, Age, Course, Marks, Joined Date and Active Status fields.
- Implemented a meaningful `__str__()` method.
- Created and applied database migrations.
- Registered Student model in Django Admin.
- Created a superuser.
- Added student records through the admin panel.
- Created a student list page using Django templates.
- Displayed active students and total student count.
- Implemented Pass/Fail status based on marks.

### Task 5: Django Form - Add Student

- Created StudentForm using Django ModelForm.
- Created an Add Student page.
- Implemented form validation.
- Added custom validation for Age (16–60).
- Added custom validation for Marks (0–100).
- Implemented database saving using `form.save()`.
- Redirected to student list after successful submission.
- Displayed form validation errors.
- Added navigation links between pages.
- Implemented success messages using Django Messages Framework.

## 7. Problems Faced

- Faced an AttributeError while calculating the student count using the model instead of the queryset.
- Faced issues displaying success notifications after form submission.
- Understood the importance of placing Django messages in the redirected page template.
- Worked with Django ModelForm validation and custom validation methods.


## 8. Topics Learned

- Django Models and Model Fields.
- Django ORM and Database Operations.
- Makemigrations and Migrate.
- Django Admin Panel.
- Superuser Creation.
- Django Views and URL Routing.
- Templates, Context and Template Inheritance concepts.
- Template Loops and Conditional Statements.
- Django ModelForm.
- Form Validation and Custom Validation.
- GET and POST Requests.
- CSRF Token.
- Redirect and Render.
- Django Messages Framework.
- Basic HTML and CSS.

## 9. Pending Work

- Review the complete project and fix any remaining issues.

## Project Status

Task 4: Django Models and Admin Panel
Task 5: Django ModelForm and Student Creation
**Project:** Student Management System
**Framework:** Django
**Language:** Python
**Database:** SQLite (Django default)
