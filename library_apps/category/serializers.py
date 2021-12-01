"""Category serializers."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework import serializers

#Model
from library_apps.category.models import Category

class CategorySerializer(serializers.ModelSerializer):
	""" Category Serializers"""

	class Meta:
		model = Category
		fields = '__all__'