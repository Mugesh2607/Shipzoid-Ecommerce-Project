from django.db import models

class Permission(models.Model):
    module = models.CharField(max_length=100)   # Example: Master Management
    name = models.CharField(max_length=100)     # Example: State
    code = models.CharField(max_length=100, unique=True)  # Example: master_state
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions"   # 👉 Custom table name
        managed = True

    def __str__(self):
        return f"{self.module} - {self.name}"
