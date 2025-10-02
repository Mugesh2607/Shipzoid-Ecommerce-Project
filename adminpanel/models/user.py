from django.db import models
from adminpanel.models import Role  
from django.contrib.auth.models import AbstractUser, Permission

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column="role_id")  # ✅ FIX
    image = models.ImageField(upload_to='adminpanel/user/', null=True, blank=True)  # 👈 New column
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)   # Auto set on create
    updated_at = models.DateTimeField(auto_now=True)       # Auto update on change


    class Meta:
        db_table = 'users'   # Map to existing table
        managed = False      # Django won't create/drop table

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_permission(self, code):
        if self.role:
            return self.role.permissions.filter(code=code).exists()
        return False