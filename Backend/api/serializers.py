from rest_framework import serializers
from .models import DocGeneralInfo, NlpAnalysis

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
            'location', 'references', 'in_text_citations', 'word_count'
        ]