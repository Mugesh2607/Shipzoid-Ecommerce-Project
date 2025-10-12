from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from ecommerce.models import Customer  
import logging
from django.shortcuts import get_object_or_404
import time
from adminpanel.utils.encryption import encrypt_id , decrypt_id
from adminpanel.decorators import admin_login_required , permission_required

@admin_login_required
@permission_required('customer_list')
def index(request):
    heading = "Customers"
    context = {
        'heading': heading,
        'active_sidebar': 'customers', # mark the Orders menu active
    }
    return render(request ,'adminpanel/customers/index.html',context)

@admin_login_required
@permission_required('customer_list')
def get_customers(request):
    customers = Customer.objects.all().order_by('-id').values()
    data = []
    for c in customers:
        encrypted_id = encrypt_id(c['id'])  # encrypt ID
        data.append({
            'id': c['id'],
            'full_name': c['full_name'],
            'phone_number': c['phone_number'],
            'email': c['email'],
            'city': c['city'],
            'state': c['state'],
            'encrypted_id': encrypted_id
        })
    return JsonResponse({'data': data})


@admin_login_required
def customer_view(request, encrypted_id):
    customer_id = decrypt_id(encrypted_id)
    customer = get_object_or_404(Customer, id=customer_id)

    context = {
        'heading': 'Customer View',
        'active_sidebar': 'customers', # mark the Orders menu active
        'customer' : customer
    }

    return render(request, 'adminpanel/customers/view.html', context)