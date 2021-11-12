from django.db import models

class FeeCategories(models.Model):
    category_code = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)
    category_desc = models.CharField(max_length=200)
    default = models.BooleanField(default=True)
    next_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True,blank=True)

