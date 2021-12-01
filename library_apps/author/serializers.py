"""Author serializers."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework import serializers

#Model
from library_apps.author.models import Author

class AuthorSerializer(serializers.ModelSerializer):
	""" Author Serializers"""

	class Meta:
		model = Author
		fields = '__all__'