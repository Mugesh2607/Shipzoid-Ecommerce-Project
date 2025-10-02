from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.http import HttpResponse , Http404
from ecommerce.models import Customer ,Order ,OrderItem
from adminpanel.models import Category , Subcategory , Product , Brands , Tax
from django.views.decorators.http import require_POST
from ecommerce.utils.encryption import encrypt_password , decrypt_password , encrypt_id 
import re ,json
from decimal import Decimal, ROUND_HALF_UP

@require_POST
def create_customer(request):

    full_name = request.POST.get("full_name", "").strip()
    phone_number = request.POST.get("phone_number", "").strip()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    
    if not full_name or not phone_number or not password or not confirm_password:
        return JsonResponse({"message": "All fields are required"}, status=400)

    
    if password != confirm_password:
        return JsonResponse({"message": "Passwords do not match"}, status=400)

    
    if not re.match(r'^\d{10}$', phone_number):
        return JsonResponse({"message": "Phone number must be exactly 10 digits"}, status=400)

    
    if Customer.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({"message": f"Phone number {phone_number} is already registered"}, status=400)


    encrypted_password = encrypt_password(password)

    customer = Customer.objects.create(
        full_name=full_name,
        phone_number=phone_number,
        password=encrypted_password,  # hash password
        status=1
    )

    return JsonResponse({"message": "Customer account created successfully!"}, status=201)


@require_POST
def customer_login(request):
    phone_number = request.POST.get("phone_number", "").strip()
    password = request.POST.get("password", "")

    if not phone_number or not password:
        return JsonResponse({"message": "Phone and password are required"}, status=400)

    try:
        customer = Customer.objects.get(phone_number=phone_number)
    except Customer.DoesNotExist:
        return JsonResponse({"message": "Account not found"}, status=404)

    # decrypt stored password
    try:
        decrypted_pass = decrypt_password(customer.password)
    except Exception:
        return JsonResponse({"message": "Something went wrong with password"}, status=500)

    if decrypted_pass != password:
        return JsonResponse({"message": "Invalid phone number or password"}, status=401)
    
    # Save session with logged_in flag
    request.session["customer"] = {
        "customer_id": customer.id,
        "customer_name": customer.full_name,
        "customer_phone": customer.phone_number,
        "logged_in": True,
    }

    return JsonResponse({
        "message": "Login successful",
        "customer": {
            "id": customer.id,
            "name": customer.full_name,
            "phone": customer.phone_number,
        }
    }, status=200)



def customer_logout(request):

    request.session.flush()
    # Redirect to home page
    return redirect('ecommerce:home')



def myaccount(request):
    customer_session = request.session.get("customer")
    if not customer_session or not customer_session.get("logged_in"):
        return redirect("ecommerce:home")

    customer_id = customer_session.get("customer_id")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        return redirect("ecommerce:home")

    # Convert customer object to dict for JSON serialization
    customer_data = {
        "id": customer.id,
        "full_name": customer.full_name,
        "email": customer.email,
        "phone": customer.phone_number,
        "address": customer.address,
        "city": customer.city,
        "state": customer.state,
        "pin_code": customer.pincode,
    }

    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    for sub in subcategories:
        sub.encrypted_id = encrypt_id(sub.id)

    orders_data = []
    orders = Order.objects.filter(customer_id=customer_id).order_by("-id")

    for order in orders:
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

            # Get tax rate from Tax table manually
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

        # Calculate grand total (subtotal + tax), rounded to 2 decimals
        grand_total = (subtotal + total_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Parse shipping address
        try:
            shipping = json.loads(order.shipping_address) if order.shipping_address else {}
        except json.JSONDecodeError:
            shipping = {}

        orders_data.append({
            "order_id": order.id,
            "order_number": order.order_number,
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": order.customer_status,
            "shippingAddress": shipping,
            "items": items,
            "total_items": total_items,
            "subtotal": float(subtotal),
            "total_tax": float(total_tax),
            "grand_total": float(grand_total),
        })

    return render(request, "ecommerce/myaccount/index.html", {
        "categories": categories,
        "subcategories": subcategories,
        "customer": customer_data,
        "orders": orders_data,
    })



@require_POST
def change_password(request):
    try:
        data = json.loads(request.body)
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")


        customer_session = request.session.get("customer")
        if not customer_session or not customer_session.get("logged_in"):
            return redirect("ecommerce:home")

        customer_id = customer_session.get("customer_id")

        customer = Customer.objects.filter(id=customer_id).first()

        if not customer:
            return JsonResponse({"status": "error", "message": "User not found."}, status=404)

        decrypted_password  = decrypt_password(customer.password)

        # Check current password
        if current_password != decrypted_password:
            return JsonResponse({"status": "error", "message": "Current password is incorrect."}, status=400)

        # Check password confirmation
        if new_password != confirm_password:
            return JsonResponse({"status": "error", "message": "New passwords do not match."}, status=400)

        # Prevent same password reuse
        if current_password == new_password:
            return JsonResponse({"status": "error", "message": "New password cannot be the same as the current password."}, status=400)

        # Update password
        customer.password = encrypt_password(new_password)
        customer.save()

        return JsonResponse({"status": "success", "message": "Password changed successfully."}, status=200)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

@require_POST
def update_personal_information(request):
        try:
            data = json.loads(request.body)

            customer_session = request.session.get("customer")
            if not customer_session or not customer_session.get("logged_in"):
                return redirect("ecommerce:home")

            customer_id = customer_session.get("customer_id")

            customer = Customer.objects.filter(id=customer_id).first()

            customer.full_name = data.get("full_name")
            customer.email = data.get("email")
            customer.phone_number = data.get("phone")
            customer.address = data.get("address")
            customer.city = data.get("city")
            customer.pincode = data.get("pin_code")
            customer.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})