from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.http import HttpResponse
from ecommerce.models import Cart, Wishlist, Order, OrderItem , Customer
from adminpanel.utils.encryption import encrypt_id , decrypt_id
from adminpanel.models import Category , Subcategory , Product , Brands , Tax , User
import re ,json
from django.db.models import Case, When, IntegerField
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import get_object_or_404
from adminpanel.decorators import admin_login_required
from django.utils import timezone

@admin_login_required
def index(request , status):
    heading = f"{status.capitalize()} Orders"
    context = {
        'heading': heading,
        'status': status,           # current order status
        'active_sidebar': 'orders', # mark the Orders menu active
    }
    return render(request, 'adminpanel/orders/index.html', context)


@admin_login_required
def get_orders(request, status):
    # Map frontend status → database status
    status_map = {
        'pending': 'confirmed',
        'processing': 'inprogress',
        'delivered': 'delivered'
    }

    orders = Order.objects.all()

    # If not "all", filter by mapped status
    if status != "all" and status in status_map:
        orders = orders.filter(customer_status=status_map[status])


    orders = orders.annotate(
        priority=Case(
            When(customer_status='confirmed', then=0),
            default=1,
            output_field=IntegerField()
        )
    ).order_by('priority', '-created_at')  # confirmed first, then latest orders

    data = []
    for order in orders:
        try:
            customer = Customer.objects.get(id=order.customer_id)
        except Customer.DoesNotExist:
            customer = None

        data.append({
            "order_id"  : encrypt_id(order.id),
            "order_number": order.order_number,
            "status": order.customer_status,
            "total_amount": float(order.total_amount),
            "created_at": order.created_at.strftime("%d %b %Y %I:%M %p"),
            "full_name": customer.full_name if customer else None,
            "phone_number": customer.phone_number if customer else None,
        })

    return JsonResponse({"data": data}, safe=False)


@admin_login_required
def view_order(request, status, order_id):
    heading = "View Order Details"

    # Decrypt the order ID
    order_pk = decrypt_id(order_id)

    # Fetch the order
    order = get_object_or_404(Order, id=order_pk)

    # Fetch the customer
    try:
        customer = Customer.objects.get(id=order.customer_id)
    except Customer.DoesNotExist:
        customer = None

    # Prepare order items
    order_items = OrderItem.objects.filter(order_id=order.id)
    items = []
    total_items = 0
    subtotal = Decimal("0.00")
    total_tax = Decimal("0.00")

    for item in order_items:
        product = Product.objects.filter(id=item.product_id).first()
        if not product:
            continue

        original_price = Decimal(str(product.price))
        discount_value = Decimal(str(product.discount_price or 0))
        discount_type = product.discount_type

        # Get tax rate
        tax_rate = Decimal("0.00")
        if product.tax_id:
            tax_obj = Tax.objects.filter(id=product.tax_id).first()
            if tax_obj:
                tax_rate = Decimal(str(tax_obj.rate or 0))

        # Calculate discount
        if discount_value > 0:
            discount_amount = (
                (original_price * discount_value / 100)
                if discount_type == "percentage"
                else discount_value
            )
        else:
            discount_amount = Decimal("0.00")

        final_price = max(original_price - discount_amount, Decimal("0.00"))
        line_subtotal = final_price * item.quantity
        line_tax = (line_subtotal * tax_rate / 100)

        subtotal += line_subtotal
        total_tax += line_tax

        items.append({
            "product_name": product.product_name,
            "quantity": item.quantity,
            "image": product.image.url if product.image else None,
            "original_price": float(original_price),
            "discount_type": discount_type,
            "discount_value": float(discount_value),
            "final_price": float(final_price),
            "tax_rate": float(tax_rate),
            "tax_amount": float(line_tax),
            "total_price": float(line_subtotal + line_tax),
        })

        total_items += item.quantity

    # Grand total
    grand_total = (subtotal + total_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Parse shipping address
    try:
        shipping = json.loads(order.shipping_address) if order.shipping_address else {}
    except json.JSONDecodeError:
        shipping = {}


    delivery_men = User.objects.filter(role_id=4)
    # Prepare context
    context = {
        'heading': heading,
        'status': status,
        'order': order,
        'customer': customer,  # include customer details
        'items': items,
        'delivery_men' : delivery_men,
        'total_items': total_items,
        'subtotal': float(subtotal),
        'total_tax': float(total_tax),
        'grand_total': float(grand_total),
        'shipping_address': shipping,
        'payment_method': order.payment_method if hasattr(order, 'payment_method') else 'COD',
        'payment_status': order.payment_status if hasattr(order, 'payment_status') else 'Pending',
        'paid_at': order.paid_at if hasattr(order, 'paid_at') else None,
    }

    return render(request, 'adminpanel/orders/view.html', context)

@admin_login_required
def assign_delivery_man(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        delivery_man_id = request.POST.get("delivery_man_id")

        try:
            order = Order.objects.get(id=order_id)
            order.delivery_man_id = delivery_man_id
            order.customer_status = "inprogress"  # move status
            order.delivered_at = timezone.now()
            order.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})