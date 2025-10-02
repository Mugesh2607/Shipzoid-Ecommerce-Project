from django.http import JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.shortcuts import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from adminpanel.models import Product, Tax
from ecommerce.models import Cart, Wishlist, Order, OrderItem , Customer
from ecommerce.utils.encryption import encrypt_id
from ecommerce.utils.encryption import decrypt_id
import json


@require_POST
def create_order(request):
    customer_session = request.session.get("customer")

    # Check if customer is logged in
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse(
            {"success": False, "message": "Please login to proceed to checkout."},
            status=401
        )

    # Validate required fields
    required_fields = [
        "full_name", "email", "phone", "address",
        "city", "state", "pin_code", "subtotal", "tax", "total"
    ]
    for field in required_fields:
        if not request.POST.get(field):
            return JsonResponse(
                {"success": False, "message": f"{field.replace('_', ' ').title()} is required."},
                status=400
            )

    customer_id = customer_session.get("customer_id")
    if not customer_id:
        return JsonResponse({"success": False, "message": "Invalid customer."}, status=400)


    last_order = Order.objects.order_by("-id").first()
    if last_order and last_order.order_number.startswith("ORD-"):
        # Extract numeric part and increment
        last_num = int(last_order.order_number.replace("ORD-", ""))
        next_num = last_num + 1
    else:
        next_num = 1

    order_number = f"ORD-{next_num:03d}"  # Pads with zeros (e.g., ORD-001, ORD-010)


    # Update customer details with address, city, state, and pincode
    Customer.objects.filter(id=customer_id).update(
        address=request.POST.get("address"),
        city=request.POST.get("city"),
        state=request.POST.get("state"),
        pincode=request.POST.get("pin_code"),
        email = request.POST.get("email"),
    )


    # Create the Order
    order = Order.objects.create(
        order_number=order_number,
        customer_id=customer_id,
        customer_status="confirmed",
        delivery_status="pending",
        payment_status="pending",
        subtotal=request.POST.get("subtotal"),
        tax_amount=request.POST.get("tax"),
        total_amount=request.POST.get("total"),
        payment_method=request.POST.get("payment_method", "COD"),
        shipping_address=json.dumps({
            "full_name": request.POST.get("full_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "state": request.POST.get("state"),
            "pin_code": request.POST.get("pin_code"),
        }),
        placed_at=timezone.now(),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )

    # Fetch cart items for the customer
    cart_items = Cart.objects.filter(user_id=customer_id)
    if not cart_items.exists():
        return JsonResponse(
            {"success": False, "message": "Cart is empty. Please add products before placing an order."},
            status=400
        )

    # Add items to OrderItem
    for item in cart_items:
        product = get_object_or_404(Product, id=item.product_id)

        # Manually fetch tax using tax_id (integer field)
        tax_rate = 0
        if product.tax_id:
            tax_obj = Tax.objects.filter(id=product.tax_id).first()
            tax_rate = tax_obj.rate if tax_obj else 0

        OrderItem.objects.create(
            order_id=order.id,
            product_id=product.id,
            price=product.price,
            quantity=item.quantity,
            size=item.size,
            tax=tax_rate,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    # Clear the customer's cart after placing the order
    cart_items.delete()

    # Encrypt order ID for secure redirect
    encrypt_orderid = encrypt_id(order.id)

    return JsonResponse({
        "success": True,
        "message": "Order placed successfully!",
        "redirect_url": reverse("ecommerce:checkout_success", args=[encrypt_orderid])
    })


def checkout_success(request, order_id):
    decrypt_orderid = decrypt_id(order_id)
    order = Order.objects.filter(id=decrypt_orderid).first()
    
    return render(request, "ecommerce/checkout/success_page.html", {"order": order})