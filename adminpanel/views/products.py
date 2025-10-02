from django.shortcuts import render
from django.http import JsonResponse
import uuid
from django.views.decorators.http import require_POST , require_http_methods
from adminpanel.models import Subcategory  , Category ,Product , Tax , Brands
from adminpanel.decorators import admin_login_required

@admin_login_required
def index(request):
    heading = "Products"
    categories = Category.objects.filter(status=1)
    subcategories = Subcategory.objects.filter(status=1)
    taxes = Tax.objects.filter(status=1)
    brands = Brands.objects.filter(status=1)
    
    # --- Generate next product code ---
    last_product = Product.objects.order_by('-id').first()
    if last_product:
        next_id = last_product.id + 1
    else:
        next_id = 1
    product_code = f"PROD-{next_id:04d}"   # e.g. PROD-0001


    context = {
        'heading': heading,
        'categories': categories,
        'subcategories': subcategories,
        'taxes': taxes,
        'brands': brands,
        'product_code': product_code,
        'active_sidebar': 'products',  # <-- add this
    }

    return render(request ,'adminpanel/products/index.html', context)


@admin_login_required
def get_products(request):
    products = Product.objects.all().order_by('-id')
    data = []

    for p in products:
        category = Category.objects.filter(id=p.category_id).values('id', 'name').first()
        subcategory = Subcategory.objects.filter(id=p.subcategory_id).values('id', 'name').first() if p.subcategory_id else None
        brand = Brands.objects.filter(id=p.brand_id).values('id', 'name').first() if p.brand_id else None
        tax = Tax.objects.filter(id=p.tax_id).values('id', 'rate').first() if p.tax_id else None

        data.append({
            'id': p.id,
            'product_name': p.product_name,
            'product_code': p.product_code,
            'category_id': category['id'] if category else None,
            'category_name': category['name'] if category else None,
            'subcategory_id': subcategory['id'] if subcategory else None,
            'subcategory_name': subcategory['name'] if subcategory else None,
            'brand_id': brand['id'] if brand else None,
            'brand_name': brand['name'] if brand else None,
            'tax_id': tax['id'] if tax else None,
            'tax_rate': tax['rate'] if tax else None,
            'price': str(p.price),
            'discount_price': str(p.discount_price) if p.discount_price else None,
            'discount_type': p.discount_type,
            'stock_quantity': p.stock_quantity,
            'sizes': p.sizes,
            'description': p.description,
            'image': p.image.url if p.image else None  # ✅ Use .url
        })

    return JsonResponse({'data': data})



@admin_login_required
def generate_product_code():
    last_product = Product.objects.order_by('-id').first()
    if last_product and last_product.product_code.startswith("PROD-"):
        last_code = int(last_product.product_code.split('-')[1])
        return f"PROD-{last_code + 1:04d}"
    return "PROD-0001"

ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]


@admin_login_required
@require_POST
def add_product(request):
    try:
        errors = {}

        # Required fields
        product_name = request.POST.get("product_name", "").strip()
        category_id = request.POST.get("category_id")
        price = request.POST.get("price")
        stock_quantity = request.POST.get("stock_quantity")

        # Optional fields
        subcategory_id = request.POST.get("subcategory_id") or None
        brand_id = request.POST.get("brand_id") or None
        tax_id = request.POST.get("tax_id") or None
        discount_price = request.POST.get("discount_price") or None
        discount_type = request.POST.get("discount_type") or None
        sizes = request.POST.get("sizes") or None
        description = request.POST.get("description") or None

        # ✅ Backend validations
        if not product_name:
            errors["product_name"] = "Product name is required."
        else:
            # Unique product name validation
            if Product.objects.filter(product_name__iexact=product_name).exists():
                errors["product_name"] = "Product name already exists."

        if not category_id:
            errors["category_id"] = "Category is required."

        # price validation
        if not price:
            errors["price"] = "Price is required."
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors["price"] = "Price must be greater than 0."
            except ValueError:
                errors["price"] = "Invalid price format."

        # stock validation
        if stock_quantity is None or stock_quantity == "":
            errors["stock_quantity"] = "Stock is required."
        else:
            try:
                stock_quantity = int(stock_quantity)
                if stock_quantity < 0:
                    errors["stock_quantity"] = "Stock cannot be negative."
            except ValueError:
                errors["stock_quantity"] = "Stock must be a number."

        # discount validation
        if discount_price:
            try:
                discount_price = float(discount_price)
                if discount_price < 0:
                    errors["discount_price"] = "Discount cannot be negative."
                elif "price" not in errors and discount_price >= price:
                    errors["discount_price"] = "Discount must be less than price."
            except ValueError:
                errors["discount_price"] = "Invalid discount format."

            if not discount_type:
                errors["discount_type"] = "Discount type required if discount price is given."

        # Image validation
        image = request.FILES.get("image")
        if not image:
            errors["image"] = "Product image is required."
        else:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_IMAGE_TYPES:
                errors["image"] = "Invalid image type. Allowed: jpg, jpeg, png"

        # return errors if any
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        # ✅ Generate Product Code here itself
        product_code = generate_product_code()

        if image:
            ext = image.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            image.name = unique_filename  # Replace original filename



        # ✅ Save Product
        product = Product.objects.create(
            product_name=product_name,
            product_code=product_code,
            category_id=category_id,
            subcategory_id=subcategory_id,
            brand_id=brand_id,
            tax_id=tax_id,
            price=price,
            discount_price=discount_price,
            discount_type=discount_type,
            stock_quantity=stock_quantity,
            sizes=sizes,
            description=description,
            image=image  # Important! Save image here
        )

        return JsonResponse({
            "message": "Product added successfully",
            "product_code": product.product_code,
            "id": product.id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@admin_login_required
@require_POST
def edit_product(request):
    try:
        product_id = request.POST.get("id")
        if not product_id:
            return JsonResponse({"error": "Product ID is required."}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)

        errors = {}

        # Required fields
        product_name = request.POST.get("product_name", "").strip()
        category_id = request.POST.get("category_id")
        price = request.POST.get("price")
        stock_quantity = request.POST.get("stock_quantity")

        # Optional fields
        subcategory_id = request.POST.get("subcategory_id") or None
        brand_id = request.POST.get("brand_id") or None
        tax_id = request.POST.get("tax_id") or None
        discount_price = request.POST.get("discount_price") or None
        discount_type = request.POST.get("discount_type") or None
        sizes = request.POST.get("sizes") or None
        description = request.POST.get("description") or None

        # Unique product name validation
        if Product.objects.exclude(id=product_id).filter(product_name__iexact=product_name).exists():
            errors["product_name"] = "Product name already exists."

        # Basic validations
        if not product_name:
            errors["product_name"] = "Product name is required."
        if not category_id:
            errors["category_id"] = "Category is required."
        if not price:
            errors["price"] = "Price is required."
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors["price"] = "Price must be greater than 0."
            except ValueError:
                errors["price"] = "Invalid price format."
        if stock_quantity is None or stock_quantity == "":
            errors["stock_quantity"] = "Stock is required."
        else:
            try:
                stock_quantity = int(stock_quantity)
                if stock_quantity < 0:
                    errors["stock_quantity"] = "Stock cannot be negative."
            except ValueError:
                errors["stock_quantity"] = "Stock must be a number."

        # Discount validation
        if discount_price:
            try:
                discount_price = float(discount_price)
                if discount_price < 0:
                    errors["discount_price"] = "Discount cannot be negative."
                elif "price" not in errors and discount_price >= price:
                    errors["discount_price"] = "Discount must be less than price."
            except ValueError:
                errors["discount_price"] = "Invalid discount format."

            if not discount_type:
                errors["discount_type"] = "Discount type required if discount price is given."

        # Image validation
        image = request.FILES.get("image")
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_IMAGE_TYPES:
                errors["image"] = "Invalid image type. Allowed: jpg, jpeg, png"

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        # Save image if uploaded


        # Update product
        product.product_name = product_name
        product.category_id = category_id
        product.subcategory_id = subcategory_id
        product.brand_id = brand_id
        product.tax_id = tax_id
        product.price = price
        product.discount_price = discount_price
        product.discount_type = discount_type
        product.stock_quantity = stock_quantity
        product.sizes = sizes
        product.description = description

        # Handle image upload if a new image is provided
        if image:
            # Optional: delete old image file
            if product.image:
                product.image.delete(save=False)

            # ✅ Generate unique filename
            ext = image.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            image.name = unique_filename

            product.image = image


        product.save()

        return JsonResponse({"message": "Product updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@admin_login_required
@require_http_methods(["POST", "DELETE"])
def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)

        # ✅ Delete image file if it exists
        if product.image:
            product.image.delete(save=False)  # removes file from MEDIA_ROOT
            
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)    