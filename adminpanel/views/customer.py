from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from ecommerce.models import Customer  
import logging
import time
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
    return JsonResponse({'data': list(customers)}, safe=False)