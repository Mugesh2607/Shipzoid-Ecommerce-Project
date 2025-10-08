from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.http import HttpResponse
from ecommerce.models import Cart, Wishlist, Order, OrderItem , Customer
from adminpanel.decorators import admin_login_required
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

@admin_login_required
def index(request):
    
    user_session = request.session.get("user")
    if not user_session or not user_session.get("logged_in"):
        return redirect("adminpanel:login")

    heading = "Dashboard Overview"
    
    # Get current datetime in project timezone
    now = timezone.localtime(timezone.now())

    # Month date ranges
    start_cur = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_next = (start_cur + timedelta(days=32)).replace(day=1)
    start_prev = (start_cur - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Helper functions
    def revenue(start, end):
        return (
            Order.objects.filter(
                customer_status='delivered',
                created_at__gte=start,
                created_at__lt=end
            ).aggregate(total=Sum('total_amount'))['total'] or 0
        )

    def count_by_status(status, start, end):
        return Order.objects.filter(
            customer_status=status,
            created_at__gte=start,
            created_at__lt=end
        ).count()

    def total_orders_count(start, end):
        return Order.objects.filter(created_at__gte=start, created_at__lt=end).count()

    def percent_change(current, last):
        return round(((current - last) / last) * 100, 2) if last > 0 else 0

    # ===== Revenue =====
    curr_rev = revenue(start_cur, start_next)
    prev_rev = revenue(start_prev, start_cur)
    percent_rev = percent_change(curr_rev, prev_rev)

    # ===== Delivered Orders =====
    curr_delivered = count_by_status('delivered', start_cur, start_next)
    prev_delivered = count_by_status('delivered', start_prev, start_cur)
    percent_delivered = percent_change(curr_delivered, prev_delivered)

    # ===== Active Orders =====
    curr_active = count_by_status('inprogress', start_cur, start_next)
    prev_active = count_by_status('inprogress', start_prev, start_cur)
    percent_active = percent_change(curr_active, prev_active)

    # ===== Total Orders =====
    total_orders_cur = total_orders_count(start_cur, start_next)
    total_orders_prev = total_orders_count(start_prev, start_cur)
    percent_total_orders = percent_change(total_orders_cur, total_orders_prev)

    # ===== Delivered Rate =====
    delivered_rate_cur = round((curr_delivered / total_orders_cur) * 100, 2) if total_orders_cur > 0 else 0
    delivered_rate_prev = round((prev_delivered / total_orders_prev) * 100, 2) if total_orders_prev > 0 else 0
    percent_delivered_rate = percent_change(delivered_rate_cur, delivered_rate_prev)

    # ===== Context =====
    context = {
        'heading': heading,
        'active_sidebar': 'dashboard_overview',

        # Revenue
        'current_month_revenue': round(curr_rev, 2),
        'percentage_revenue_change': percent_rev,

        # Delivered Orders
        'current_delivered_orders': curr_delivered,
        'percentage_delivered_change': percent_delivered,

        # Active Orders
        'active_orders': curr_active,
        'percentage_active_change': percent_active,

        # Total Orders
        'total_orders': total_orders_cur,
        'percentage_total_orders_change': percent_total_orders,

        # Delivered Rate
        'delivered_rate': delivered_rate_cur,
        'percentage_delivered_rate_change': percent_delivered_rate,
    }


    if user_session.get("role_id") == 4:
        # Delivery Man Dashboard
        return render(request, "adminpanel/dashboard/deliveryman-dashboard.html", context)
    else:
        # Default Admin / Other Role Dashboard
        return render(request, "adminpanel/dashboard/index.html", context)
   
