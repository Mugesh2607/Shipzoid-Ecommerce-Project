from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Brands  
import logging
import time
from adminpanel.decorators import admin_login_required

@admin_login_required
def index(request):
    heading = "Brands"
    
    context = {
        'heading': heading,
        'active_sidebar': 'brands',  # <-- mark sidebar as active
    }
    return render(request ,'adminpanel/brands/index.html',context)

@admin_login_required
def get_brands(request):
    brands = Brands.objects.all().order_by('-id').values('id', 'name', 'status')
    return JsonResponse({'data': list(brands)})


@admin_login_required
@require_POST
def add_brand(request):
    name = request.POST.get('name')
    status = request.POST.get('status', 0)

    if not name:
        return JsonResponse({'error': 'Brand name is required'}, status=400)
    
      # Validation: Max 255 characters
    if len(name) > 255:
        return JsonResponse({'error': 'Brand name must be at most 255 characters'}, status=400)

    if Brands.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Brand already exists'}, status=400)

    Brands.objects.create(name=name, status=status)
    return JsonResponse({'message': 'Brand added successfully'})


@admin_login_required
@require_POST
def edit_brand(request):
    brand_id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status', 0)

    # Ensure the category exists
    try:
        brand = Brands.objects.get(id=brand_id)
    except Brands.DoesNotExist:
        return JsonResponse({'error': 'Brand not found'}, status=404)

    # Validation: Required field
    if not name:
        return JsonResponse({'error': 'Brand name is required'}, status=400)

    name = name.strip()  # remove extra spaces

    # Validation: Max 255 characters
    if len(name) > 255:
        return JsonResponse({'error': 'Brand name must be at most 255 characters'}, status=400)

    # Validation: Unique name excluding current category
    if Brands.objects.filter(name__iexact=name).exclude(id=brand_id).exists():
        return JsonResponse({'error': 'Brand already exists'}, status=400)

    # Update the category
    brand.name = name
    brand.status = status
    brand.save()

    return JsonResponse({'message': 'Brand updated successfully'})


@admin_login_required
@require_http_methods(["POST", "DELETE"])
def delete_brand(request, id):
    try:
        brand = Brands.objects.get(id=id)
        brand.delete()
        return JsonResponse({'message': 'Brand deleted successfully'})
    except Brands.DoesNotExist:
        return JsonResponse({'error': 'Brand not found'}, status=404)