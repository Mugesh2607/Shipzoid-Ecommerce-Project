from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from adminpanel.models import User

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.session.get("user")
        if not user or not user.get("logged_in"):
            return redirect('adminpanel:login')  # or '/admin/login/'
        return view_func(request, *args, **kwargs)
    return wrapper



def permission_required(code):
    """Decorator to check permissions for a view"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_dict = request.session.get("user")

            # If not logged in
            if not user_dict or not user_dict.get("logged_in"):
                messages.warning(request, "Please log in to continue.")
                return redirect('adminpanel:login')  # your login URL name

            try:
                user = User.objects.get(id=user_dict["id"])
            except User.DoesNotExist:
                messages.error(request, "User not found. Please log in again.")
                return redirect('adminpanel:login')

            # Correct logic: only allow if user has permission
            if not user.has_permission(code):
                messages.error(request, "You don't have permission to access this page.")
                return redirect('adminpanel:login') # or redirect("dashboard")

            # If permission granted → allow view
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator