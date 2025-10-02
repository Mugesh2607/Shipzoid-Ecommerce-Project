from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse , Http404
from django.core.paginator import Paginator
from adminpanel.models import Category , Subcategory , Product , Brands
from ecommerce.models import Cart , Wishlist
from ecommerce.utils.encryption import encrypt_id
from ecommerce.utils.encryption import decrypt_id

def index(request):
    categories = Category.objects.filter(status=1)
    subcategories = Subcategory.objects.filter(status=1)

    for sub in subcategories:
        sub.encrypted_id = encrypt_id(sub.id)

    return render(request, 'ecommerce/home/index.html' , {'categories' : categories , 'subcategories' : subcategories})


def product_list(request):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 8))


    customer_session = request.session.get("customer")
    customer_id = customer_session.get("customer_id") if customer_session else None

    # Fetch wishlist items only if customer is logged in
    wishlist_product_ids = set()
    if customer_id:
        wishlist_items = Wishlist.objects.filter(user_id=customer_id)
        wishlist_product_ids = set(w.product_id for w in wishlist_items)


    # Build a safe brand lookup dictionary
    brand_map = {
        b.id: b.name
        for b in Brands.objects.filter(status=1)
    }

    products = Product.objects.all().order_by("id")  # stable order (no duplicates/shuffling)
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page)

    data = []
    for p in page_obj:
        brand_name = brand_map.get(p.brand_id, "")  # fallback to empty string


        data.append({
            "id": p.id,
            "name": p.product_name,
            "price": float(p.price),
            "image": p.image.url if p.image else "",
            "discount" : p.discount_price if p.discount_price else "",
            "discount_type" : p.discount_type if p.discount_type else "",
            "sizes" : p.sizes if p.sizes else "",
            "description": getattr(p, "description", ""),
            "brand_name": brand_name,
            "is_in_wishlist": p.id in wishlist_product_ids
        })

    return JsonResponse({
        "products": data,
        "has_next": page_obj.has_next()
    })


def subcategory(request ,enc_id):

    categories = Category.objects.filter(status=1)
    subcategories = Subcategory.objects.filter(status=1)


    for sub in subcategories:
        sub.encrypted_id = encrypt_id(str(sub.id))

    try:
        subcategory_id = decrypt_id(enc_id)
    except Exception:
        raise Http404("Subcategory not found")
    

    products = Product.objects.filter(subcategory_id=subcategory_id)

    # Get distinct brands from these products with status=1
    brand_ids = products.values_list('brand_id', flat=True).distinct()
    brands = Brands.objects.filter(id__in=brand_ids, status=1)

    return render(request, 'ecommerce/subcategory/index.html' , {'categories' : categories , 'subcategories' : subcategories , 'encrypt_id' : enc_id , 'brands': brands})


def subcategoryproduct_list(request, enc_id):
    # ---------------------------
    # 🔹 Decrypt subcategory id safely
    # ---------------------------
    try:
        subcategory_id = decrypt_id(enc_id)
    except Exception:
        raise Http404("Invalid Subcategory")

    # ---------------------------
    # 🔹 Pagination values
    # ---------------------------
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 8))

    # ---------------------------
    # 🔹 Base query for products
    # ---------------------------
    products = Product.objects.filter(subcategory_id=subcategory_id)

    # ---------------------------
    # 🔹 Apply Brand Filters (if provided)
    # ---------------------------
    brands_param = request.GET.get("brands", "").strip()
    if brands_param:
        brand_ids = [int(b) for b in brands_param.split(",") if b.isdigit()]
        if brand_ids:
            products = products.filter(brand_id__in=brand_ids)

    # ---------------------------
    # 🔹 Apply Price Filter (if provided)
    # ---------------------------
    price_param = request.GET.get("price", "").strip()
    if price_param.isdigit():
        products = products.filter(price__lte=int(price_param))

    # ---------------------------
    # 🔹 Final ordering
    # ---------------------------
    products = products.order_by("id")

    # ---------------------------
    # 🔹 Handle Wishlist (if logged in)
    # ---------------------------
    customer_id = request.session.get("customer", {}).get("customer_id")
    wishlist_product_ids = set()
    if customer_id:
        wishlist_product_ids = set(
            Wishlist.objects.filter(user_id=customer_id).values_list("product_id", flat=True)
        )

    # ---------------------------
    # 🔹 Build Brand Lookup Map
    # ---------------------------
    brand_map = {b.id: b.name for b in Brands.objects.filter(status=1)}

    # ---------------------------
    # 🔹 Pagination
    # ---------------------------
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page)

    # ---------------------------
    # 🔹 Build Response Data
    # ---------------------------
    data = [
        {
            "id": p.id,
            "name": p.product_name,
            "price": float(p.price),
            "image": p.image.url if p.image else "",
            "discount": p.discount_price or "",
            "discount_type": p.discount_type or "",
            "sizes": p.sizes or "",
            "description": getattr(p, "description", ""),
            "is_in_wishlist": p.id in wishlist_product_ids,
            "brand_name": brand_map.get(p.brand_id, ""),
        }
        for p in page_obj
    ]

    # ---------------------------
    # 🔹 Return JSON response
    # ---------------------------
    return JsonResponse({
        "products": data,
        "has_next": page_obj.has_next()
    })
