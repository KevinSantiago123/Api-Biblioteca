"""Editorial serializers."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework import serializers

#Model
from library_apps.editorial.models import Editorial

class EditorialSerializer(serializers.ModelSerializer):
	"""Editorial Serializers"""

	class Meta:
		model = Editorial
		fields = '__all__'