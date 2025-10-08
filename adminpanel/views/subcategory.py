from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Subcategory  , Category
from adminpanel.decorators import admin_login_required , permission_required
import logging
import time

@admin_login_required
@permission_required('subcategory_list')
def index(request):
    heading = "Subcategory"
    categories = Category.objects.filter(status=1)

    context = {
        'heading': heading,
        'categories' : categories,
        'active_sidebar': 'subcategory',  # <-- mark sidebar as active
    }
    return render(request ,'adminpanel/subcategory/index.html',context)

@admin_login_required
@permission_required('subcategory_list')
def get_subcategories(request):
    subcategories = Subcategory.objects.all().order_by('-id').values(
        'id', 'name', 'status', 'category_id'
    )

    data = []
    for sub in subcategories:
        # fetch category for this subcategory
        category = Category.objects.filter(id=sub['category_id']).values('id', 'name').first()

        sub['category'] = category if category else None
        data.append(sub)

    return JsonResponse({'data': data})

@admin_login_required
@permission_required('subcategory_add')
@require_POST
def add_subcategory(request):
    name = request.POST.get('name')
    status = request.POST.get('status', 0)
    category_id = request.POST.get('category_id')

    # Validation
    if not name:
        return JsonResponse({'error': 'Subcategory name is required'}, status=400)

    if len(name) > 255:
        return JsonResponse({'error': 'Subcategory name must be at most 255 characters'}, status=400)

    if not category_id:
        return JsonResponse({'error': 'Category is required'}, status=400)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Selected category does not exist'}, status=400)

    if Subcategory.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Subcategory already exists'}, status=400)

    # Create Subcategory with category relation
    Subcategory.objects.create(name=name, status=status, category_id=category.id)

    return JsonResponse({'message': 'Subcategory added successfully'})

@admin_login_required
@permission_required('subcategory_edit')
@require_POST
def edit_subcategory(request):
    subcategory_id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status', 0)
    category_id = request.POST.get('category_id')

    # Ensure the category exists
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
    except Subcategory.DoesNotExist:
        return JsonResponse({'error': 'Subcategory not found'}, status=404)

    # Validation: Required field
    if not name:
        return JsonResponse({'error': 'Subcategory name is required'}, status=400)
    
    if not category_id:
        return JsonResponse({'error': 'Category is required'}, status=400)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Selected category does not exist'}, status=400)

    name = name.strip()  # remove extra spaces

    # Validation: Max 255 characters
    if len(name) > 255:
        return JsonResponse({'error': 'Subcategory name must be at most 255 characters'}, status=400)

    # Validation: Unique name excluding current category
    if Subcategory.objects.filter(name__iexact=name).exclude(id=subcategory_id).exists():
        return JsonResponse({'error': 'Subcategory already exists'}, status=400)

    # Update the category
    subcategory.name = name
    subcategory.status = status
    subcategory.category_id = category_id
    subcategory.save()

    return JsonResponse({'message': 'Subcategory updated successfully'})


@admin_login_required
@permission_required('subcategory_delete')
@require_http_methods(["POST", "DELETE"])
def delete_subcategory(request, id):
    try:
        subcategory = Subcategory.objects.get(id=id)
        subcategory.delete()
        return JsonResponse({'message': 'Subcategory deleted successfully'})
    except Subcategory.DoesNotExist:
        return JsonResponse({'error': 'SubCategory not found'}, status=404)