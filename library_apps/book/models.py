#Django
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.base import Model


#Models
from library_apps.editorial.models import Editorial
from library_apps.author.models import Author
from library_apps.category.models import Category

class Book(models.Model):
    """Model Class Book."""

    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, blank=False, null=False)
    subtitulo = models.CharField(max_length=150, blank=False, null=False)
    fecha_publicacion = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(max_length=8000, blank=False, null=False)
    id_editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)

class LibroAutor(models.Model):
    """Model Class Book-Author."""

    id_libro_autor = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_autor = models.ForeignKey(Author, on_delete=models.CASCADE)

class LibroCategory(models.Model):
    """Model Class Book-Author."""

    id_libro_categoria = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Category, on_delete=models.CASCADE)


