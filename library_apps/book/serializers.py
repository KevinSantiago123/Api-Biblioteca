"""Book serializers."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework import serializers

#Models
from library_apps.book.models import Book, LibroAutor, LibroCategory


class BookSerializer(serializers.Serializer):
	""" Book Serializers"""

	id_libro = serializers.IntegerField(required=False)
	titulo = serializers.CharField(max_length=100, required=False)
	subtitulo = serializers.CharField(max_length=150, required=False)
	fecha_publicacion = serializers.CharField(max_length=50, required=False)
	descripcion = serializers.CharField(max_length=8000, required=False)
	id_editorial = serializers.IntegerField(required=False)

	class Meta:
		model = Book

class GoogleSerializer(serializers.Serializer):
	id = serializers.CharField(max_length=40)
	source = serializers.CharField(max_length=40)

class LibroAuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = LibroAutor
		fields = '__all__'

class LibroCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = LibroCategory
		fields = '__all__'

class BookResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'
