from django.http import JsonResponse
from django.views.decorators.http import require_POST , require_GET
from adminpanel.models import Product , Tax
from ecommerce.models import Cart , Wishlist

@require_POST
def add_to_cart(request):
    try:
        product_id = request.POST.get('product_id')
        size = request.POST.get('size', '')
        quantity = int(request.POST.get('quantity', 1))

        # Get customer session dict
        customer_session = request.session.get("customer")

        if not customer_session or not customer_session.get("logged_in"):
            return JsonResponse({'success': False, 'message': 'Please login to add items to cart.'}, status=401)

        customer_id = customer_session.get("customer_id")

        # Validate quantity
        if quantity < 1:
            return JsonResponse({'success': False, 'message': 'Quantity must be at least 1.'})

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})

        # Check if product already exists for this user
        cart_item = Cart.objects.filter(
            user_id=customer_id,
            product_id=product.id
        ).first()

        if cart_item:
            # If size is different, update size
            if cart_item.size != size:
                cart_item.size = size
                cart_item.quantity = quantity  # reset quantity for new size
                message = 'Cart updated with new size.'
            else:
                # Same size, just update quantity
                cart_item.quantity += quantity
                message = 'Cart quantity updated.'
            cart_item.save()
        else:
            # Create new entry if product not in cart
            Cart.objects.create(
                user_id=customer_id,
                product_id=product.id,
                size=size,
                quantity=quantity
            )
            message = 'Added to cart successfully.'

        return JsonResponse({'success': True, 'message': message})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})



def get_cart_items(request):
    # Get customer session
    customer_session = request.session.get("customer")

    # Check login
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse({'success': False, 'message': 'Please login to view cart.'}, status=401)

    customer_id = customer_session.get("customer_id")

    # Get cart items for this customer
    cart_items = Cart.objects.filter(user_id=customer_id)
    data = []

    for item in cart_items:
        # Manually find the product using the stored product_id
        product = Product.objects.filter(id=item.product_id).first()
        if not product:
            # Skip if product doesn't exist
            continue

        # Fetch tax details from Tax table
        tax = Tax.objects.filter(id=product.tax_id).first()

        base_price = product.price

        # ---- Apply discount ----
        if product.discount_type == 'percentage':
            discounted_price = base_price - (base_price * (product.discount_price / 100))
        elif product.discount_type == 'amount':
            discounted_price = base_price - product.discount_price
        else:
            discounted_price = base_price

        # Ensure price never goes below zero
        discounted_price = max(discounted_price, 0)

        final_price = discounted_price

        # Add cart item to response
        data.append({
            "id": item.id,
            "product_id": product.id,
            "name": product.product_name,
            "image": product.image.url if product.image else "",
            "quantity": item.quantity,
            "size": item.size,
            "price": round(final_price, 2)
        })

    return JsonResponse({"success": True, "cart": data})



@require_POST
def remove_from_cart(request, id):
    customer_session = request.session.get("customer")

    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse({'success': False, 'message': 'Please login to manage your cart.'}, status=401)

    try:
        cart_item = Cart.objects.get(id=id, user_id=customer_session.get("customer_id"))
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Item removed from cart.'})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
    


def update_cart_quantity(request, id):
    if request.method == "POST":
        try:
            # Ensure user is logged in
            customer_session = request.session.get("customer")
            if not customer_session or not customer_session.get("logged_in"):
                return JsonResponse({'success': False, 'message': 'Please login to update cart.'}, status=401)

            customer_id = customer_session.get("customer_id")
            quantity = int(request.POST.get('quantity', 1))

            if quantity < 1:
                return JsonResponse({'success': False, 'message': 'Quantity must be at least 1.'})

            cart_item = Cart.objects.filter(user_id=customer_id, id=id).first()
            if not cart_item:
                return JsonResponse({'success': False, 'message': 'Cart item not found.'}, status=404)

            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({'success': True, 'message': 'Cart updated successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



@require_POST
def add_to_wishlist(request):
    try:
        customer_session = request.session.get("customer")
        if not customer_session or not customer_session.get("logged_in"):
            return JsonResponse({'success': False, 'message': 'Please login to add wishlist.'}, status=401)
    

        product_id = request.POST.get("product_id")
        size = request.POST.get("size", "")
        quantity = int(request.POST.get("quantity", 1))
        customer_id = customer_session.get("customer_id")

        if not product_id:
            return JsonResponse({"success": False, "message": "Invalid product."}, status=400)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return JsonResponse({"success": False, "message": "Product not found."}, status=404)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user_id=customer_id,
            product_id=product_id,
            size=size,
            defaults={"quantity": quantity}
        )

        if not created:
            wishlist_item.quantity = quantity
            wishlist_item.save()
            message = "Wishlist item updated successfully."
        else:
            message = "Item added to wishlist."

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)
    

@require_GET
def get_wishlist(request):
    # Check customer session
    customer_session = request.session.get("customer")
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse(
            {'success': False, 'message': 'Please login to view wishlist.', 'count': 0, 'items': []},
            status=401
        )

    customer_id = customer_session.get("customer_id")
    wishlist_items = Wishlist.objects.filter(user_id=customer_id)

    data = []
    for item in wishlist_items:
        product = Product.objects.filter(id=item.product_id).first()
        if not product:
            continue

        base_price = product.price

        # Apply discount if present
        if product.discount_type == 'percentage':
            discounted_price = base_price - (base_price * (product.discount_price / 100))
        elif product.discount_type == 'amount':
            discounted_price = base_price - product.discount_price
        else:
            discounted_price = base_price

        final_price = max(discounted_price, 0)

        data.append({
            "id": item.id,
            "product_id": product.id,
            "name": product.product_name,
            "image": product.image.url if product.image else "/static/images/placeholder.png",
            "price": round(float(final_price), 2),
            "rating": round(1)
        })

    return JsonResponse({
        "success": True,
        "count": wishlist_items.count(),
        "items": data
    })



@require_POST
def remove_from_wishlist(request, item_id):
    customer_session = request.session.get("customer")
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse({'success': False, 'message': 'Please login to view wishlist.'}, status=401)

    customer_id = customer_session.get("customer_id")

    # Try to delete the wishlist item
    deleted, _ = Wishlist.objects.filter(id=item_id, user_id=customer_id).delete()

    if deleted:
        return JsonResponse({"success": True, "message": "Removed from wishlist"})
    else:
        return JsonResponse({"success": False, "message": deleted}, status=404)



@require_POST
def remove_wishlist_by_product(request, item_id):
    customer_session = request.session.get("customer")
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse({'success': False, 'message': 'Please login to view wishlist.'}, status=401)

    customer_id = customer_session.get("customer_id")

    # Try to delete the wishlist item
    deleted, _ = Wishlist.objects.filter(product_id=item_id, user_id=customer_id).delete()

    if deleted:
        return JsonResponse({"success": True, "message": "Removed from wishlist"})
    else:
        return JsonResponse({"success": False, "message": deleted}, status=404)


@require_POST
def add_to_cart_from_wishlist(request, item_id):
    # Check if customer is logged in via session
    customer_session = request.session.get("customer")
    if not customer_session or not customer_session.get("logged_in"):
        return JsonResponse(
            {'success': False, 'message': 'Please login to move items to your cart.'},
            status=401
        )

    customer_id = customer_session.get("customer_id")

    # Get wishlist item for this user
    wishlist_item = Wishlist.objects.filter(id=item_id, user_id=customer_id).first()
    if not wishlist_item:
        return JsonResponse({"success": False, "message": "Wishlist item not found."}, status=404)

    # Check if product exists
    product = Product.objects.filter(id=wishlist_item.product_id).first()
    if not product:
        return JsonResponse({"success": False, "message": "Product no longer available."}, status=404)

    # Check if item is already in the cart with the same size
    existing_cart_item = Cart.objects.filter(
        user_id=customer_id,
        product_id=wishlist_item.product_id,
        size=wishlist_item.size
    ).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # Create a new cart entry including size
        Cart.objects.create(
            user_id=customer_id,
            product_id=wishlist_item.product_id,
            quantity=1,
            size=wishlist_item.size
        )

    # Remove item from wishlist after adding to cart
    wishlist_item.delete()

    return JsonResponse({"success": True, "message": "Item moved to cart successfully."})