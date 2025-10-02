from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Category  
import logging
import time
from adminpanel.decorators import admin_login_required

@admin_login_required
def index(request):
    heading = "Category"
    context = {
        'heading': heading,
        'active_sidebar': 'category',  # <-- mark sidebar as active
    }
    return render(request ,'adminpanel/category/category.html',context)

@admin_login_required
def get_categories(request):
    categories = Category.objects.all().order_by('-id').values('id', 'name', 'status')
    return JsonResponse({'data': list(categories)})


@admin_login_required
@require_POST
def add_category(request):
    name = request.POST.get('name')
    status = request.POST.get('status', 0)

    if not name:
        return JsonResponse({'error': 'Category name is required'}, status=400)
    
      # Validation: Max 255 characters
    if len(name) > 255:
        return JsonResponse({'error': 'Category name must be at most 255 characters'}, status=400)

    if Category.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Category already exists'}, status=400)

    Category.objects.create(name=name, status=status)
    return JsonResponse({'message': 'Category added successfully'})


@admin_login_required
@require_POST
def edit_category(request):
    category_id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status', 0)

    # Ensure the category exists
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    # Validation: Required field
    if not name:
        return JsonResponse({'error': 'Category name is required'}, status=400)

    name = name.strip()  # remove extra spaces

    # Validation: Max 255 characters
    if len(name) > 255:
        return JsonResponse({'error': 'Category name must be at most 255 characters'}, status=400)

    # Validation: Unique name excluding current category
    if Category.objects.filter(name__iexact=name).exclude(id=category_id).exists():
        return JsonResponse({'error': 'Category already exists'}, status=400)

    # Update the category
    category.name = name
    category.status = status
    category.save()

    return JsonResponse({'message': 'Category updated successfully'})

logger = logging.getLogger(__name__)


@admin_login_required
@require_http_methods(["POST", "DELETE"])
def delete_category(request, id):
    logger.info(f"Delete request received for category id={id} at {time.time()}")
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return JsonResponse({'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    