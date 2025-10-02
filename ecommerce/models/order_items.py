from django.db import models
from django.utils import timezone


class OrderItem(models.Model):
    order_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=50, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "order_items"
        managed = False

    def __str__(self):
        return f"Item {self.id} of Order {self.order_id}"