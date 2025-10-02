from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

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
            if not user_dict or not user_dict.get("logged_in"):
                return HttpResponseForbidden("Permission denied")
            
            from adminpanel.models import User
            try:
                user = User.objects.get(id=user_dict["id"])
            except User.DoesNotExist:
                return HttpResponseForbidden("Permission denied")
            
            if user.has_permission(code):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Permission denied")
        return _wrapped_view
    return decorator