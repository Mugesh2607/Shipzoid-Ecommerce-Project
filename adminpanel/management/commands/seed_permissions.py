# app/management/commands/seed_permissions.py
from django.core.management.base import BaseCommand
from adminpanel.models.permission import Permission  # import your Permission model

class Command(BaseCommand):
    help = "Seed initial permissions"

    def handle(self, *args, **kwargs):
        permissions = [
            # User
            {"module": "User Management", "name": "User List", "code": "users_list"},
            {"module": "User Management", "name": "User Add", "code": "user_add"},
            {"module": "User Management", "name": "User Edit", "code": "user_edit"},
            {"module": "User Management", "name": "User Delete", "code": "user_delete"},

            #Roles
            {"module": "User Management", "name": "Role List", "code": "role_list"},
            {"module": "User Management", "name": "Role Add", "code": "role_add"},
            {"module": "User Management", "name": "Role Edit", "code": "role_edit"},
            {"module": "User Management", "name": "Role Delete", "code": "role_delete"},

            #Products
            {"module": "Inventory Management", "name": "Products List", "code": "product_list"},
            {"module": "Inventory Management", "name": "Products Add", "code": "product_add"},
            {"module": "Inventory Management", "name": "Products Edit", "code": "product_edit"},
            {"module": "Inventory Management", "name": "Products Delete", "code": "product_delete"},

            #Category
            {"module": "Inventory Management", "name": "Category List", "code": "category_list"},
            {"module": "Inventory Management", "name": "Category Add", "code": "category_add"},
            {"module": "Inventory Management", "name": "Category Edit", "code": "category_edit"},
            {"module": "Inventory Management", "name": "Category Delete", "code": "category_delete"},

            #Subcategory
            {"module": "Inventory Management", "name": "Subcategory List", "code": "subcategory_list"},
            {"module": "Inventory Management", "name": "Subcategory Add", "code": "subcategory_add"},
            {"module": "Inventory Management", "name": "Subcategory Edit", "code": "subcategory_edit"},
            {"module": "Inventory Management", "name": "Subcategory Delete", "code": "subcategory_delete"},


            #Brands
            {"module": "Inventory Management", "name": "Brand List", "code": "brand_list"},
            {"module": "Inventory Management", "name": "Brand Add", "code": "brand_add"},
            {"module": "Inventory Management", "name": "Brand Edit", "code": "brand_edit"},
            {"module": "Inventory Management", "name": "Brand Delete", "code": "brand_delete"},


            #Taxes
            {"module": "Inventory Management", "name": "Tax List", "code": "tax_list"},
            {"module": "Inventory Management", "name": "Tax Add", "code": "tax_add"},
            {"module": "Inventory Management", "name": "Tax Edit", "code": "tax_edit"},
            {"module": "Inventory Management", "name": "Tax Delete", "code": "tax_delete"},


            #orders
            {"module": "Order Management", "name": "Order List", "code": "order_list"},
            {"module": "Order Management", "name": "Order View", "code": "order_view"},

            #Business
            {"module": "Business Management", "name": "Customer List", "code": "customer_list"},
            {"module": "Business Management", "name": "Customer View", "code": "customer_view"},

            #Reports
            {"module": "Report Management", "name": "Revenue Report", "code": "revenue_report"},

            #Settings
            {"module": "Settings Management", "name": "Settings", "code": "settings"},
        ]

        for perm in permissions:
            Permission.objects.get_or_create(
                module=perm["module"],
                name=perm["name"],
                code=perm["code"]
            )

        self.stdout.write(self.style.SUCCESS("All permissions seeded successfully"))
