from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.views.decorators.http import require_POST , require_GET
from adminpanel.models import Category , Subcategory , Product , Brands , Tax
from ecommerce.models import Cart , Wishlist ,Customer
from ecommerce.utils.encryption import encrypt_id
from ecommerce.utils.encryption import decrypt_id

from decimal import Decimal, ROUND_HALF_UP

def index(request):
    customer_session = request.session.get("customer")

    if not customer_session or not customer_session.get("logged_in"):
        return redirect('ecommerce:home')

    customer_id = customer_session.get("customer_id")
    customer = Customer.objects.filter(id=customer_id).first()

    cart_items = Cart.objects.filter(user_id=customer_id)
    cart_data = []
    cart_subtotal = Decimal('0.00')
    cart_tax_total = Decimal('0.00')

    for item in cart_items:
        product = Product.objects.filter(id=item.product_id).first()
        if not product:
            continue

        tax = Tax.objects.filter(id=product.tax_id).first()
        tax_rate = Decimal(tax.rate) if tax else Decimal('0')

        base_price = Decimal(product.price)

        # Apply discount
        if product.discount_type == 'percentage':
            discounted_price = base_price - (base_price * (Decimal(product.discount_price) / Decimal('100')))
        elif product.discount_type == 'amount':
            discounted_price = base_price - Decimal(product.discount_price)
        else:
            discounted_price = base_price

        final_price = max(discounted_price, Decimal('0'))

        # Total price for this item
        total_price = (final_price * item.quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Tax amount
        tax_amount = (total_price * (tax_rate / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Totals
        cart_subtotal += total_price - tax_amount
        cart_tax_total += tax_amount

        cart_data.append({
            "id": item.id,
            "product_id": product.id,
            "name": product.product_name,
            "image": product.image.url if product.image else "",
            "quantity": item.quantity,
            "size": item.size,
            "price": final_price.quantize(Decimal('0.01')),
            "total_price": total_price
        })

    # Grand total
    cart_total = sum(Decimal(item['price']) * item['quantity'] for item in cart_data)

    return render(request, 'ecommerce/checkout/index.html', {
        'customer': customer,
        'cart_items': cart_data,
        'cart_subtotal': cart_subtotal.quantize(Decimal('0.01')),
        'cart_tax_total': cart_tax_total.quantize(Decimal('0.01')),
        'cart_total': cart_total.quantize(Decimal('0.01'))
    })
