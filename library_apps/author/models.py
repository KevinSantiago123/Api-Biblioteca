from django.db import models

class Author(models.Model):
    """Model Class Author Book."""

    id_autor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=False, null=False)