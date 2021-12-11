from django.db import models

class GradingSchemes(models.Model):
    scheme_code = models.AutoField(primary_key=True)
    scheme_name = models.CharField(max_length=200)
