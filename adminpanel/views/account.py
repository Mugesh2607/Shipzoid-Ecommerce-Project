from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Category  
import logging
import time
from adminpanel.decorators import admin_login_required 

@admin_login_required
def index(request):
    heading = "My Account"
    context = {
        'heading': heading
    }
    return render(request ,'adminpanel/account/index.html',context)


    