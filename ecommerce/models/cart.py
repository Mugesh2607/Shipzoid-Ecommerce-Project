from django.db import models

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.BigIntegerField()
    size = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'  # maps to existing table
        managed = False    # Django won't try to create or alter the table