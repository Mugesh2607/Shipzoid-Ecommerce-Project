from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.http import HttpResponse
from adminpanel.decorators import admin_login_required

@admin_login_required
def index(request):
    
    user_session = request.session.get("user")
    if not user_session or not user_session.get("logged_in"):
        return redirect("adminpanel:login")

    heading = "Dashboard Overview"
    context = {
        'heading': heading,          
        'active_sidebar': 'dashboard_overview', # mark the Orders menu active
    }
    
    if user_session.get("role_id") == 4:
        # Delivery Man Dashboard
        return render(request, "adminpanel/dashboard/deliveryman-dashboard.html", context)
    else:
        # Default Admin / Other Role Dashboard
        return render(request, "adminpanel/dashboard/index.html", context)
   
