from django.urls import path
from . import views


app_name = 'adminpanel';

urlpatterns  = [
    path("" ,views.dashboard.index , name="dashboard") ,
    path("login/" ,views.login.index , name="login") ,
    path("signup/" ,views.login.signup , name="signup") ,
    path("logout/" ,views.login.logout , name="logout") ,
    path("login/authenticate/" ,views.login.authenticate_user , name="authenticate") ,

    # Users URLS
    path("user/" ,views.users.index , name="users") ,
    path("add-user/" ,views.users.add_user , name="add_user") ,
    path('users/', views.users.get_users, name='get_users'),
    path('edit-user/', views.users.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.users.delete_user, name='delete_user'),

    # Category URLS
    path("category/" ,views.category.index , name="category") ,
    path("add-category/" ,views.category.add_category , name="add_category") ,
    path("edit-category/" ,views.category.edit_category , name="edit_category") ,
    path('delete-category/<int:id>/', views.category.delete_category, name='delete_category'),
    path('categories/', views.category.get_categories, name='get_categories'),

    #Sub Category URLS
    path("subcategory/" ,views.subcategory.index , name="subcategory") ,
    path('subcategories/', views.subcategory.get_subcategories, name='get_subcategories'),
    path("add-subcategory/" ,views.subcategory.add_subcategory , name="add_subcategory") ,
    path("edit-subcategory/" ,views.subcategory.edit_subcategory , name="edit_subcategory") ,
    path('delete-subcategory/<int:id>/', views.subcategory.delete_subcategory, name='delete_subcategory'),


    #Brands URLS
    path("brands/" ,views.brands.index , name="brands") ,
    path('get-brands/', views.brands.get_brands, name='get_brands'),
    path("add-brand/" ,views.brands.add_brand , name="add_brand") ,
    path("edit-brand/" ,views.brands.edit_brand , name="edit_brand") ,
    path('delete-brand/<int:id>/', views.brands.delete_brand, name='delete_brand'),

    #Taxes URLS
    path("taxes/" ,views.tax.index , name="taxes") ,
    path('get-taxes/', views.tax.get_taxes, name='get_taxes'),
    path("add-tax/" ,views.tax.add_tax , name="add_tax") ,
    path("edit-tax/" ,views.tax.edit_tax , name="edit_tax") ,
    path('delete-tax/<int:id>/', views.tax.delete_tax, name='delete_tax'),

    #Products URLS
    path("products/" ,views.products.index , name="products") ,
    path("add-product/" ,views.products.add_product , name="add_product") ,
    path('get-products/', views.products.get_products, name='get_products'),
    path("edit-product/" ,views.products.edit_product , name="edit_product") ,
    path('delete-product/<int:id>/', views.products.delete_product, name='delete_product'),

    #Roles URLS
    path("roles/" ,views.roles.index , name="roles") ,
    path("add-role/" ,views.roles.add_role , name="add_role") ,
    path('get-roles/', views.roles.get_roles, name='get_roles'),
    path("edit-role/" ,views.roles.edit_role , name="edit_role") ,
    path('delete-role/<int:id>/', views.roles.delete_role, name='delete_role'),
    path('get-role-permissions/<int:role_id>/', views.roles.get_role_permissions, name='get_role_permissions'),


    #Customer URLS
    path("customers/" ,views.customer.index , name="customers") ,
    path('get-customers/', views.customer.get_customers, name='get_customers'),

    #Order URLS
   path("orders/<str:status>/", views.orders.index, name="orders"),
   path('get-orders/<str:status>/', views.orders.get_orders, name='get_orders'),
   path('view-order/<str:status>/<str:order_id>', views.orders.view_order, name='view_order'),
   path('assign-deliverman/', views.orders.assign_delivery_man, name='assign_delivery_man'),



    #Delivery Man URLS
   path("delivery-orders/<str:status>/", views.delivery_man.index, name="assigned_orders"),
   path('get-delivery-orders/<str:status>/', views.delivery_man.get_orders, name='get_delivery_orders'),
   path('deliveryman-order-view/<str:status>/<str:order_id>', views.delivery_man.view_order, name='deliveryman_view_order'),
   path('complete-delivery/', views.delivery_man.complete_delivery, name='complete_delivery'),
]