from django.db import models

class Editorial(models.Model):
    """Model Class Category Book."""

    id_editorial = models.AutoField(primary_key=True)
    editorial = models.CharField(max_length=150, blank=False, null=False)