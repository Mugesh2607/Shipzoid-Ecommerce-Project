from django.db import models

class Tax(models.Model):
    name = models.CharField(max_length=255)   # Tax name (e.g. GST 18%)
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # Tax percentage (e.g. 18.00)
    status = models.IntegerField(default=1)  # 1 = Active, 0 = Inactive
    created_at = models.DateTimeField(auto_now_add=True)   # Auto set on create
    updated_at = models.DateTimeField(auto_now=True)       # Auto update on change

    class Meta:
        db_table = 'taxes'   # Match the table name in DB
        managed = False      # Django won't create/drop the table

    def __str__(self):
        return f"{self.name} ({self.rate}%)"
