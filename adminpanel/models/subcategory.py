from django.db import models

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name = models.CharField(max_length=255, unique=True)  # Subcategory name
    category_id = models.IntegerField(default=0)  # Example: 0 = inactive, 1 = active
    status = models.IntegerField(default=0)  # Example: 0 = inactive, 1 = active
    created_at = models.DateTimeField(auto_now_add=True)  # Set on insert
    updated_at = models.DateTimeField(auto_now=True)      # Set on update

    class Meta:
        db_table = 'subcategories'  # Match existing DB table
        managed = False  # Django won't create or modify this table

    def __str__(self):
        return self.name
