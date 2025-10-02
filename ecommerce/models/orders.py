from django.db import models
from django.utils import timezone
from adminpanel.models import User


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer_id = models.BigIntegerField()
    customer_status = models.CharField(max_length=50)
    delivery_status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.JSONField(null=True, blank=True)
    delivery_man = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,   # if delivery man is deleted, set null
        null=True, 
        blank=True,
        related_name='assigned_orders',
        db_column='delivery_man_id'
    )
    placed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    delivered_at = models.DateTimeField(null=True, blank=True)

    delivery_remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "orders"
        managed = True

    def __str__(self):
        return f"Order {self.order_number}"