from django.http import JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.shortcuts import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from adminpanel.models import Product, Tax
from ecommerce.models import Cart, Wishlist, Order, OrderItem , Customer
from ecommerce.utils.encryption import encrypt_id
from ecommerce.utils.encryption import decrypt_id
from django.conf import settings
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

    send_order_email(
        customer_email=request.POST.get("email"),
        full_name=request.POST.get("full_name"),
        order_number=order_number,
        total_amount=request.POST.get("total")
    )

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



#Mail Send Section
def send_order_email(customer_email, full_name, order_number, total_amount):
    subject = f"Your Shipzoid Order Confirmation - {order_number}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [customer_email]

    # Fallback plain text
    text_content = f"Hi {full_name}, your order {order_number} for ₹{total_amount} has been placed successfully."

    # HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; margin:0; padding:0;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="20" cellspacing="0" style="background-color: #ffffff; border-radius: 10px;">
                        <tr>
                            <td style="text-align: center; background-color: #1e40af; color: white; border-radius: 10px 10px 0 0;">
                                <h1>Shipzoid</h1>
                                <p>Order Confirmation</p>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p>Hi <strong>{full_name}</strong>,</p>
                                <p>Thank you for shopping with <strong>Shipzoid</strong>! Your order has been successfully placed.</p>
                                <p><strong>Order Number:</strong> {order_number}</p>
                                <p><strong>Total Amount:</strong> ₹{total_amount}</p>
                                <p>We are processing your order and will notify you once it is shipped.</p>
                                <hr>
                                <p style="font-size: 12px; color: gray;">
                                    Shipzoid - Fast, Reliable, and Secure Shopping.<br>
                                    www.shipzoid.com
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Order email sent successfully!")
    except Exception as e:
        print("Email sending failed:", e)