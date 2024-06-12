from rest_framework import serializers
from .models import DocGeneralInfo

# Serializer will translate the data into JSON format so we can visualize it in the frontend
class DocGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocGeneralInfo
        fields = '__all__'
