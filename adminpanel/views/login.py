from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.http import HttpResponse
from adminpanel.models import User
from adminpanel.utils.encryption import encrypt_password , decrypt_password  
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'adminpanel/auth/login.html')

@csrf_exempt
def authenticate_user(request):
    """Authenticate login and handle session"""
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": {"__all__": [{"message": "Invalid request method"}]}}, status=400)

    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    remember_me = request.POST.get("rememberme")  # "on" if checked
    errors = {}

    # ✅ Validation
    if not email:
        errors["email"] = [{"message": "Email is required"}]
    if not password:
        errors["password"] = [{"message": "Password is required"}]

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        errors["__all__"] = [{"message": "Invalid email or password"}]
        return JsonResponse({"success": False, "errors": errors}, status=400)

    decrypted_password = decrypt_password(user.password)

    # Compare entered vs decrypted
    if password != decrypted_password:
        errors["__all__"] = [{"message": "Invalid email or password"}]
        return JsonResponse({"success": False, "errors": errors}, status=400)
    

    request.session["user"] = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "name": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "image": user.image.url if user.image else None,
        "status": user.status,
        "role_id": user.role.id if user.role else None,
        "role_name": user.role.name if user.role else None,
        "logged_in": True
    }

    # ✅ Handle Remember Me
    if remember_me == "on":
        request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
    else:
        request.session.set_expiry(0)  # Expire on browser close

    return JsonResponse({
        "success": True,
        "redirect_url": "/admin/"   # redirect after login
    })


def logout(request):
    # Clear all session data
    request.session.flush()
    # Redirect to login page
    return redirect('adminpanel:login')

def signup(request):
    return render(request, 'adminpanel/auth/signup.html')
