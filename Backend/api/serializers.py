from rest_framework import serializers
from .models import DocGeneralInfo, NlpAnalysis

#Serializers allow complex data such as querysets and model instances to be converted to 
#native Python datatypes that can then be easily rendered into JSON, XML or other content types.
class DocGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocGeneralInfo
        fields = ['general_info_id', 'date_submitted', 'source', 'title', 'author', 'nlp_id']
        read_only_fields = ['general_info_id', 'nlp_id', 'date_submitted']

class NlpAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = NlpAnalysis
        fields = [
            'nlp_id', 'document_type', 'keywords', 'summary', 'document_date', 'category',
            'related_documents', 'status', 'language', 'version', 'confidentiality_level',
            'location', 'references', 'uploaded_by', 'approval_status', 'related_projects'
        ]