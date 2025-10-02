from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=100, unique=True)

    category_id = models.IntegerField()  # or ForeignKey to Category model
    subcategory_id = models.IntegerField(null=True, blank=True)  # or ForeignKey
    brand_id = models.IntegerField(null=True, blank=True)        # or ForeignKey
    tax_id = models.IntegerField(null=True, blank=True)          # or ForeignKey

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=50, null=True, blank=True)  # 'flat' / 'percent'

    stock_quantity = models.IntegerField(default=0)
    sizes = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='adminpanel/products/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        managed = False

    def __str__(self):
        return f"{self.product_name} ({self.product_code})"
