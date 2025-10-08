from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Role  , Permission
from adminpanel.decorators import admin_login_required , permission_required

@admin_login_required
@permission_required('role_list')
def index(request):
    heading = "Roles"
    permissions = Permission.objects.all().order_by('module', 'name')
    modules = {}
    for perm in permissions:
        if perm.module not in modules:
            modules[perm.module] = []
        modules[perm.module].append(perm)


    context = {
        'heading': heading,
        'modules': modules,
        'active_sidebar': 'roles', 
    }



    return render(request ,'adminpanel/roles/index.html',context)

@admin_login_required
@permission_required('role_list')
def get_roles(request):
    roles = Role.objects.all().order_by('-id').values('id', 'name', 'status')
    return JsonResponse({'data': list(roles)})

@admin_login_required
@permission_required('role_add')
@require_POST
def add_role(request):
    name = request.POST.get('name')
    status = request.POST.get('status', 0)
    permissions = request.POST.getlist('permissions')  # List of permission IDs

    if not name:
        return JsonResponse({'error': 'Role name is required'}, status=400)
    
      # Validation: Max 255 characters
    if len(name) > 100:
        return JsonResponse({'error': 'Role name must be at most 255 characters'}, status=400)

    if Role.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Role already exists'}, status=400)

    role = Role.objects.create(name=name, status=status)

    if permissions:
        role.permissions.set(permissions)
    
    return JsonResponse({'message': 'Role added successfully'})


@admin_login_required
@permission_required('role_edit')
@require_POST
def edit_role(request):
    role_id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status', 0)
    permissions = request.POST.getlist('permissions')  # List of permission IDs

    # Ensure the category exists
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)

    # Validation: Required field
    if not name:
        return JsonResponse({'error': 'Role name is required'}, status=400)

    name = name.strip()  # remove extra spaces

    # Validation: Max 255 characters
    if len(name) > 100:
        return JsonResponse({'error': 'Role name must be at most 255 characters'}, status=400)

    # Validation: Unique name excluding current category
    if Role.objects.filter(name__iexact=name).exclude(id=role_id).exists():
        return JsonResponse({'error': 'Role already exists'}, status=400)

    # Update the category
    role.name = name
    role.status = status
    role.save()

    if permissions:
        role.permissions.set(permissions)
    else:
        role.permissions.clear()  # remove all if none selected
    return JsonResponse({'message': 'Role updated successfully'})

@admin_login_required
@permission_required('role_delete')
@require_http_methods(["POST", "DELETE"])
def delete_role(request, id):
    try:
        role = Role.objects.get(id=id)
        role.delete()
        return JsonResponse({'message': 'Role deleted successfully'})
    except Role.DoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)
    


def get_role_permissions(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
        permission_ids = list(role.permissions.values_list('id', flat=True))
        return JsonResponse({"success": True, "permissions": permission_ids})
    except Role.DoesNotExist:
        return JsonResponse({"success": False, "permissions": []})