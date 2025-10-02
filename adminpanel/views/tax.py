from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Tax  
from adminpanel.decorators import admin_login_required
from decimal import Decimal, InvalidOperation

@admin_login_required
def index(request):
    heading = "Taxes"
    context = {
        'heading': heading,
        'active_sidebar': 'taxes',  # <-- mark sidebar as active
    }
    return render(request ,'adminpanel/taxes/index.html',context)

@admin_login_required
def get_taxes(request):
    taxes = Tax.objects.all().order_by('-id').values('id', 'name', 'rate' , 'status')
    return JsonResponse({'data': list(taxes)})

@admin_login_required
@require_POST
def add_tax(request):
    name = request.POST.get('name')
    rate = request.POST.get('percentage')
    status = request.POST.get('status', 0)

    # --- Validate Name ---
    if not name:
        return JsonResponse({'error': 'Tax name is required'}, status=400)

    if len(name) > 255:
        return JsonResponse({'error': 'Tax name must be at most 255 characters'}, status=400)

    # --- Validate Percentage (rate) ---
    if not rate:
        return JsonResponse({'error': 'Tax percentage is required'}, status=400)

    try:
        rate = Decimal(rate)  # convert safely
    except InvalidOperation:
        return JsonResponse({'error': 'Tax percentage must be a valid number'}, status=400)

    # percentage range validation (0–100)
    if rate < 0 or rate > 100:
        return JsonResponse({'error': 'Tax percentage must be between 0 and 100'}, status=400)

    # --- Validate Status ---
    try:
        status = int(status)
    except ValueError:
        status = 0
    if status not in [0, 1]:
        return JsonResponse({'error': 'Invalid status value'}, status=400)


    # --- Save ---
    Tax.objects.create(name=name, rate=rate, status=status)

    return JsonResponse({'message': 'Tax added successfully'})

@admin_login_required
@require_POST
def edit_tax(request):
    tax_id = request.POST.get('id')
    name = request.POST.get('name')
    rate = request.POST.get('percentage')
    status = request.POST.get('status', 0)

    # --- Validate ID ---
    if not tax_id:
        return JsonResponse({'error': 'Tax ID is required'}, status=400)

    try:
        tax = Tax.objects.get(id=tax_id)
    except Tax.DoesNotExist:
        return JsonResponse({'error': 'Tax not found'}, status=404)

    # --- Validate Name ---
    if not name:
        return JsonResponse({'error': 'Tax name is required'}, status=400)

    if len(name) > 255:
        return JsonResponse({'error': 'Tax name must be at most 255 characters'}, status=400)


    # --- Validate Percentage (rate) ---
    if not rate:
        return JsonResponse({'error': 'Tax percentage is required'}, status=400)

    try:
        rate = Decimal(rate)  # safely convert
    except InvalidOperation:
        return JsonResponse({'error': 'Tax percentage must be a valid number'}, status=400)

    if rate < 0 or rate > 100:
        return JsonResponse({'error': 'Tax percentage must be between 0 and 100'}, status=400)

    # --- Validate Status ---
    try:
        status = int(status)
    except ValueError:
        status = 0

    if status not in [0, 1]:
        return JsonResponse({'error': 'Invalid status value'}, status=400)

    # --- Save Changes ---
    tax.name = name
    tax.rate = rate
    tax.status = status
    tax.save(update_fields=['name', 'rate', 'status', 'updated_at'])

    return JsonResponse({'message': 'Tax updated successfully'})

@admin_login_required
@require_http_methods(["POST", "DELETE"])
def delete_tax(request, id):
    try:
        tax = Tax.objects.get(id=id)
        tax.delete()
        return JsonResponse({'message': 'Tax deleted successfully'})
    except Tax.DoesNotExist:
        return JsonResponse({'error': 'Tax not found'}, status=404)