from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Role   , User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from adminpanel.decorators import admin_login_required , permission_required
from adminpanel.utils.encryption import encrypt_password , decrypt_password
import uuid

@admin_login_required
@permission_required('users_list')
def index(request):
    heading = "Users"
    roles = Role.objects.filter(status=1)
    context = {
        'active_sidebar': 'users',
        'heading': heading,
        'roles': roles
    }
    return render(request ,'adminpanel/users/index.html',context)

@admin_login_required
@permission_required('users_list')
def get_users(request):
    users = User.objects.select_related("role").order_by("-id")


    data = []
    for u in users:
        data.append({
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "phone": u.phone,
            "address": u.address,
            "password": '',
            "role_name": u.role.name if u.role else "N/A",
            "role_id": u.role.id if u.role else "N/A",
            "password" : decrypt_password(u.password) ,
            "status": u.status,
            'profile_image': u.image.url if u.image else None  # ✅ Use .url
        })

    return JsonResponse({"data": data})


ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
@admin_login_required
@permission_required('user_add')
@require_POST
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        role_id = request.POST.get("role")
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        status = request.POST.get("status", 1)

        # Backend validations
        if not first_name:
            return JsonResponse({"error": "First name is required!"}, status=400)
        if not email:
            return JsonResponse({"error": "Email is required!"}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists!"}, status=400)
        
        if not phone:
            return JsonResponse({"error": "Phone number is required!"}, status=400)

        if User.objects.filter(phone=phone).exists():
            return JsonResponse({"error": "Phone number already exists!"}, status=400)

        if len(password) < 6:
            return JsonResponse({"error": "Password must be at least 6 characters!"}, status=400)
        
        if not role_id:  
            return JsonResponse({"error": "Role is required!"}, status=400)

        if not role_id or not Role.objects.filter(id=role_id).exists():
            return JsonResponse({"error": "Invalid role selected!"}, status=400)
        
        # Image validation
        image = request.FILES.get("profile_image")
        if not image:
            return JsonResponse({"error": "User image is required!"}, status=400)
        else:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_IMAGE_TYPES:
                return JsonResponse({"error": "Invalid image type. Allowed: jpg, jpeg, png"}, status=400)


        if image:
            ext = image.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            image.name = unique_filename  # Replace original filename

        # Save User
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=encrypt_password(password),  # Hash password
            role_id=role_id,
            phone=phone,
            address=address,
            status=status,
            image=image  # Important! Save image here
        )

        return JsonResponse({"message": "User added successfully!", "user_id": user.id}, status=201)

    return JsonResponse({"error": "Invalid request method!"}, status=405)

@admin_login_required
@permission_required('user_edit')
@require_POST
def edit_user(request):
    try:
        user_id = request.POST.get("id")
        if not user_id:
            return JsonResponse({"error": "User ID is required!"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found!"}, status=404)

        # Collect fields
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        role_id = request.POST.get("role")
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        status = request.POST.get("status", "1")

        # 🔹 Validations
        if not first_name:
            return JsonResponse({"error": "First name is required!"}, status=400)

        if not email:
            return JsonResponse({"error": "Email is required!"}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format!"}, status=400)

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({"error": "Email already exists!"}, status=400)
        

        if not phone:
            return JsonResponse({"error": "Phone number is required!"}, status=400)

        if User.objects.filter(phone=phone).exclude(id=user.id).exists():
            return JsonResponse({"error": "Phone number already exists!"}, status=400)

        if role_id and not Role.objects.filter(id=role_id).exists():
            return JsonResponse({"error": "Invalid role selected!"}, status=400)

        # Image validation
        image = request.FILES.get("profile_image")
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_IMAGE_TYPES:
                return JsonResponse(
                    {"error": "Invalid image type. Allowed: jpg, jpeg, png"},
                    status=400
                )

        # 🔹 Update fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        user.status = int(status)

        if role_id:
            user.role_id = role_id

        # Handle image upload
        if image:
            # Delete old image if exists
            if user.image:
                user.image.delete(save=False)

            # Generate unique filename
            ext = image.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            image.name = unique_filename

            user.image = image

        # Update password if provided
        if password:
            if len(password) < 6:
                return JsonResponse(
                    {"error": "Password must be at least 6 characters!"}, status=400
                )
            user.password = encrypt_password(password)

        user.save()

        return JsonResponse(
            {"message": "User updated successfully!", "user_id": user.id}, status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@admin_login_required
@permission_required('user_delete')
@require_http_methods(["POST", "DELETE"])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
        
        # ✅ Delete image file if it exists
        if user.image:
            user.image.delete(save=False)  # removes file from MEDIA_ROOT


        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)