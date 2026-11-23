from django.http import HttpResponseForbidden
from functools import wraps
from .models import UserProfile
from django.shortcuts import redirect

# role custum decorator
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                role = request.user.profile.role
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden("Access Denied")

            if role not in allowed_roles:
                return HttpResponseForbidden("You are not authorized!")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
