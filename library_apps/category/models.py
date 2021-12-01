from django.db import models

class Category(models.Model):
    """Model Class Category Book."""

    id_categoria = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=100, blank=False, null=False)