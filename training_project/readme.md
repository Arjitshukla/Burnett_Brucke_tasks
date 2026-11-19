# Student Management System

A Django-based web application to manage student records with CRUD functionality, role-based access control, secure authentication, and account management.

## 1. Project Setup

### Clone Repository

```bash
git clone <repository-url>
cd "main Interships/training_project/my_project"
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

Open in browser:

http://127.0.0.1:8000/

## 4. Application URLs

| URL | Description |
|---|---|
| `/admin/` | Django Admin Panel |
| `/students/` | Display All Students |
| `/students/<id>/` | Student Details |
| `/students/add/` | Add Student |
| `/students/<id>/edit/` | Edit Student |
| `/students/<id>/delete/` | Delete Student |
| `/students/login/` | User Login |
| `/students/register/` | User Registration |
| `/students/logout/` | User Logout |
| `/students/password-reset/` | Request Password Reset |
| `/students/password-reset/done/` | Password Reset Email Confirmation |
| `/students/reset/<uidb64>/<token>/` | Set New Password |
| `/students/reset/done/` | Password Reset Complete |

## 5. Tasks Completed

### Task 1: Role-Based Authentication and Dashboard Design

- Implemented role-based authentication for Administrator, Trainer, and Student.
- Created separate dashboards for all three roles.
- Implemented reusable Django templates.
- Used Bootstrap for consistent page design.
- Added role-specific navigation and access controls.
- Implemented protected views using role-based permissions.

### Task 2: Secure Account Management

**Registration and Authentication**
- Implemented user registration, login, and logout.
- Added email uniqueness validation.
- Implemented trainer account approval.
- Added administrator-controlled account activation and deactivation.

**Password Security**
- Implemented minimum 8-character password validation.
- Added uppercase, lowercase, digit, and special character requirements.
- Prevented passwords similar to username and email.
- Implemented password and confirmation matching.
- Used Django built-in password validators wherever possible.
- Implemented secure password change functionality.

**Password Reset**
- Implemented password reset using Django built-in authentication views.
- Added password reset email templates.
- Implemented password reset confirmation and completion pages.

**Login Protection**
- Tracked failed login attempts using the UserProfile model.
- Temporarily blocked accounts after five failed attempts.
- Implemented a 15-minute account lock.
- Displayed Bootstrap alerts for login errors and account lock messages.

**Audit Logging**
- Created an AuditLog model to record authentication events.
- Recorded successful login, failed login, account lock, and blocked login events.
- Registered AuditLog in Django Admin for viewing records.

**Session and Cookie Security**
- Studied SESSION_COOKIE_HTTPONLY.
- Studied SESSION_COOKIE_SECURE.
- Studied CSRF_COOKIE_SECURE.
- Studied SESSION_EXPIRE_AT_BROWSER_CLOSE.
- Studied SESSION_COOKIE_AGE.
- Documented HTTPS requirements for secure-cookie settings and their limitations during local HTTP development.

### Task 4: Django Models and Admin

- Created Student model with required fields.
- Applied migrations and registered model in Django Admin.
- Added student records through Admin.
- Implemented student list, active students, and Pass/Fail status.

### Task 5: Django ModelForm

- Created StudentForm using ModelForm.
- Implemented Add Student functionality.
- Added Age (16–60) and Marks (0–100) validation.
- Implemented validation errors and success messages.

### Task 6: Student CRUD Operations

- Implemented List, Detail, Add, Edit, and Delete functionality.
- Created a delete confirmation page.
- Used separate views, URLs, and templates.
- Implemented redirects and validation error handling.

## 6. Role and Permission Matrix

The Student Management System uses Role-Based Access Control (RBAC) with three roles: Administrator, Trainer, and Student.

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
- Passwords are handled using Django's authentication and password hashing mechanisms.
- Login protection and audit logging help track suspicious authentication activity.

## 7. Login Protection — Documentation

### Current Limitations

- Failed login attempts are tracked per username, not per IP address.
- Audit logs currently store basic event information.
- Database-based tracking may require concurrency protection for simultaneous requests.

### Production Improvements

- Use Redis or distributed caching for scalable login-attempt tracking.
- Implement username-based and IP-based rate limiting.
- Use centralized logging and monitoring.
- Generate security alerts for suspicious activities.
- Protect audit logs against unauthorized modification and deletion.

## 8. Session and Cookie Security

### Important Django Settings

| Setting | Purpose |
|---|---|
| `SESSION_COOKIE_HTTPONLY` | Prevents JavaScript from accessing the session cookie. |
| `SESSION_COOKIE_SECURE` | Sends session cookies only over HTTPS. |
| `CSRF_COOKIE_SECURE` | Sends CSRF cookies only over HTTPS. |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | Controls session expiration when the browser closes. |
| `SESSION_COOKIE_AGE` | Defines session lifetime in seconds. |

### Local Development vs Production

During local HTTP development, secure-cookie settings should generally remain disabled:

```python
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

In production with HTTPS enabled:

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

These settings should not be blindly enabled during local HTTP development because browsers may not send secure cookies over HTTP.

## 9. Topics Learned

- Django Models, ORM, and Migrations.
- Django Admin and Superuser.
- Views, URLs, and Templates.
- ModelForm and Custom Validation.
- GET and POST Requests.
- CRUD Operations.
- `get_object_or_404()`.
- Django Messages Framework.
- Redirect and Render.
- Django Authentication System.
- Password Hashing and Validation.
- Role-Based Access Control (RBAC).
- Django Sessions and Cookies.
- Password Reset and Password Change.
- Login Attempt Tracking.
- Audit Logging.
- Django Security Best Practices.
- Bootstrap Forms and Alerts.

---

**Technology Stack:** Python, Django, SQLite/PostgreSQL, HTML, CSS, Bootstrap, JavaScript, Git.