from rest_framework import serializers
from .models import DocGeneralInfo, NlpAnalysis, User, Case
#Serializers allow complex data such as querysets and model instances to be converted to 
#native Python datatypes that can then be easily rendered into JSON, XML or other content types.
class DocGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocGeneralInfo
        fields = ['_id','general_info_id', 'date_submitted', 'source', 'title', 'author', 'nlp_id']
        read_only_fields = ['general_info_id', 'nlp_id', 'date_submitted']

class NlpAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = NlpAnalysis
        fields = ['_id',
            'nlp_id', 'document_type', 'summary',  'category',
             'language', 'ner', 'confidentiality_level',
             'references', 'in_text_citations', 'word_count'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

 
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'
 