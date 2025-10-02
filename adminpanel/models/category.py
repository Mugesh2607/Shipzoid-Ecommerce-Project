from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=0)  # changed from CharField to IntegerField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'  # Match the manual table name
        managed = False        # Django won't try to create/drop the table

    def __str__(self):
        return self.name
