from django.db import models

class CategoryAudit(models.Model):
    categoryaudit_code = models.AutoField(primary_key=True)
    categoryaudit_dateassigned = models.DateTimeField()
    categoryaudit_categoryfrom = models.CharField(max_length=200)
    categoryaudit_categoryto = models.CharField(max_length=200)
    categoryaudit_username = models.CharField(max_length=200)