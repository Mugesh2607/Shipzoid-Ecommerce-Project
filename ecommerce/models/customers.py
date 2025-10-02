from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)  # 👈 updated
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    status = models.IntegerField(default=1)  # 1 = Active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'  # Match the manual table name
        managed = False        # Django won't try to create/drop the table

    def __str__(self):
        return self.full_name