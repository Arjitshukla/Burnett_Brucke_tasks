# Student Management System

A Django-based web application to manage student records with complete CRUD functionality.

## 1. Project Setup

### Clone Repository
```bash
git clone <repository-url>
cd main Interships\training_project\my_project
```

### Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 3. Run Development Server

```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## 4. Application URLs

| URL | Description |
|---|---|
| `/admin/` | Django Admin Panel |
| `/students/` | Display All Students |
| `/students/<id>/` | Student Details |
| `/students/add/` | Add Student |
| `/students/<id>/edit/` | Edit Student |
| `/students/<id>/delete/` | Delete Student |

## 5. Tasks Completed

### Task 4: Django Models and Admin
- Created Student model with required fields.
- Applied migrations and registered model in Django Admin.
- Added student records through Admin.
- Implemented student list, active students and Pass/Fail status.

### Task 5: Django ModelForm
- Created StudentForm using ModelForm.
- Implemented Add Student functionality.
- Added Age (16–60) and Marks (0–100) validation.
- Implemented validation errors and success messages.

### Task 6: Student CRUD Operations
- Implemented List, Detail, Add, Edit and Delete functionality.
- Created a delete confirmation page.
- Used separate views, URLs and templates.
- Implemented redirects and validation error handling.

## 7. Topics Learned

- Django Models, ORM and Migrations.
- Django Admin and Superuser.
- Views, URLs and Templates.
- ModelForm and Custom Validation.
- GET and POST Requests.
- CRUD Operations.
- `get_object_or_404()`.
- Django Messages Framework.
- Redirect and Render.

## Role and Permission Matrix

The Student Management System uses role-based access control (RBAC) with three roles: Administrator, Trainer, and Student.

| Feature / Permission | Administrator | Trainer | Student |
|---|:---:|:---:|:---:|
| Manage Students | ✅ | ❌ | ❌ |
| Manage Trainers | ✅ | ❌ | ❌ |
| Manage Courses | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |
| Access Admin Dashboard | ✅ | ❌ | ❌ |
| View Assigned Courses | ✅ | ✅ | Own Courses |
| View Assigned Students | ✅ | ✅ | ❌ |
| Update Student Marks | ✅ | ✅ | ❌ |
| Add Student Feedback | ✅ | ✅ | ❌ |
| View Own Profile | ✅ | ❌ | ✅ |
| View Own Marks | ✅ | ❌ | ✅ |
| View Visible Feedback | ✅ | ❌ | ✅ |
| Access Audit Logs | ✅ | ❌ | ❌ |

### Access Control

- **Administrator:** Has administrative access to manage students, trainers, courses, users, dashboards, and audit logs.
- **Trainer:** Can view assigned courses and students, update student marks, and add feedback.
- **Student:** Can view only their own profile, enrolled courses, marks, and visible feedback.

### Security Implementation

- Role-based access is managed through the `UserProfile` model.
- Students are linked to Django User accounts.
- The `role_required` decorator protects role-specific views.
- Unauthorized requests return HTTP 403.
- Object ownership is checked to prevent unauthorized access through URL ID manipulation.
- Permissions are validated in backend views, not only by hiding template buttons.