from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wishlist'  # maps to existing table
        managed = False    # Django won't try to create or alter the table
