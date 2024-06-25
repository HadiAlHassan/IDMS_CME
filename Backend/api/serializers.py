from rest_framework import serializers
from .models import DocGeneralInfo

#Serializers allow complex data such as querysets and model instances to be converted to 
#native Python datatypes that can then be easily rendered into JSON, XML or other content types.
class DocGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocGeneralInfo
        fields = ['general_info_id', 'date_submitted', 'source', 'title', 'author', 'nlp_id']
        read_only_fields = ['general_info_id', 'nlp_id', 'date_submitted']
