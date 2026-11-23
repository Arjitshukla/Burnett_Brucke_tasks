from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from ..models import UserProfile
from ..utils import create_audit_log


# Authentication and Authorization

# Create your views here.
def home(request):
    return render(request, "students/home.html")


def about(request):
    return render(request, "students/about.html")


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "").strip()

        errors = {}
        non_field_errors = []

        # 1. Empty field validation
        if not username:
            errors['username'] = "Username is required."

        if not email:
            errors['email'] = "Email is required."

        if not password:
            errors['password'] = ["Password is required."]

        if not confirm_password:
            errors['confirm_password'] = "Confirm password is required."

        if errors:
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 2. Password matching validation
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 3. Duplicate username validation
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 4. Duplicate email validation
        if User.objects.filter(email__iexact=email).exists():
            errors['email'] = "Email already exists."
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 5. Password strength validation
        try:
            validate_password(password,user=User(username=username, email=email))
        except ValidationError as error:
            errors['password'] = error.messages
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 6. Role validation
        if role not in ['student', 'trainer']:
            non_field_errors.append("Invalid role selected.")
            return render(
                request,
                "students/registration/register.html",
                {
                    "errors": errors,
                    "non_field_errors": non_field_errors
                }
            )

        # 7. Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=(role == 'student')
        )

        # 8. Create user profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "students/registration/register.html")


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        profile = UserProfile.objects.filter(
            user__username=username
        ).first()

        # Check whether account is locked
        if profile and profile.locked_until:

            if profile.locked_until > timezone.now():

                # Audit Login attempted
                create_audit_log(
                    request,
                    "Login Blocked",
                    "Login attempted while account was locked.",
                    user=profile.user,
                    username=username
                )
                messages.error(
                    request,
                    "Account temporarily locked. Please try again later."
                )
                return render(
                    request,
                    "students/registration/login.html"
                )

            else:
                profile.failed_login_attempts = 0
                profile.locked_until = None
                profile.save()

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Reset failed attempts after successful login
            if profile:
                profile.failed_login_attempts = 0
                profile.locked_until = None
                profile.save()

            # Audit successful login
            create_audit_log(
                    request,
                    "LOGIN",
                    "User logged in successfully.",
                    user=profile.user,
                    username=username
                )
            login(request, user)
            messages.success(request, "Login successful!")

            # Role-based redirect
            try:
                role = user.profile.role

                if role == 'admin':
                    return redirect('admin_dashboard')

                elif role == 'trainer':
                    return redirect('trainer_dashboard')

                elif role == 'student':
                    return redirect('student_dashboard')

                else:
                    messages.error(request, "Invalid user role.")
                    return redirect('login')

            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('login')

        else:

            # Audit failed login
            create_audit_log(
                    request,
                    "FAILED",
                    "Invalid username or password.",
                    user=profile.user if profile else None,
                    username=username
                )
            if profile:
                profile.failed_login_attempts += 1

                if profile.failed_login_attempts >= 5:
                    profile.locked_until = (timezone.now() + timedelta(minutes=15))

                    # AduitLog for Account locked
                    create_audit_log(
                    request,
                    "Account Locked",
                    "Account locked for 15 minutes.",
                    user=profile.user,
                    username=username
                )
                    
                    messages.error(
                        request,
                        "Too many failed attempts. Account locked for 15 minutes."
                    )
                else:
                    messages.error(
                        request,
                        f"Invalid credentials. Attempts remaining: {5 - profile.failed_login_attempts}"
                    )

                profile.save()

            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "students/registration/login.html")


def logout_view(request):
    if request.user.is_authenticated:

        create_audit_log(
            request,
            "LOGOUT",
            "User logged out successfully.",
            user=request.user
        )

    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

