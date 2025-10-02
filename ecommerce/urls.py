from django.urls import path
from . import views

app_name = 'ecommerce';

urlpatterns  = [
    path("" ,views.home.index , name="home") ,
    path("ecommerce/products/", views.home.product_list, name="product_list"),
    path("s/<str:enc_id>/", views.home.subcategory, name="subcategory"),
    path("subcategory-products/<str:enc_id>/", views.home.subcategoryproduct_list, name="subcategory_products"),

    #customer login & signin URLS
    path("ecommerce/customer-create/", views.customer.create_customer, name="create_customer") ,
    path("ecommerce/customer-login/", views.customer.customer_login, name="customer_login") ,
    path("ecommerce/customer-logout/", views.customer.customer_logout, name="customer_logout") ,


    #customer Myaccount URL
    path("account/", views.customer.myaccount, name="myaccount") ,
    path('account/change-password/', views.customer.change_password, name='change_password'),
    path('account/update-personal-information/', views.customer.update_personal_information, name='update_personal_information'),

    #cart URLS
    path('cart/add/', views.cart.add_to_cart, name='add_to_cart'),
    path('get-cart-items/', views.cart.get_cart_items, name='get_cart_items'),
    path('cart/remove/<int:id>', views.cart.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:id>/', views.cart.update_cart_quantity, name='update_cart_quantity'),

    #wishlist URLS
    path("wishlist/add/", views.cart.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.cart.get_wishlist, name="get_wishlist"),
    path("wishlist/remove/<int:item_id>/", views.cart.remove_from_wishlist, name="remove_from_wishlist"),
    path("remove-wishlist/<int:item_id>/", views.cart.remove_wishlist_by_product, name="remove_wishlist_by_product"),
    path("wishlist/add-to-cart/<int:item_id>/", views.cart.add_to_cart_from_wishlist, name="add_to_cart_from_wishlist"),


    #checkout URLS
    path("checkout/", views.checkout.index, name="checkout"),

    #order URLS
    path("create-order/", views.order.create_order, name="create_order"),
    path("checkout/success/<str:order_id>/", views.order.checkout_success, name="checkout_success"),
]