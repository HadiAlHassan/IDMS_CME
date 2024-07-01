from pymongo import errors
from functools import wraps
import fitz
from bson import ObjectId

from Utils.db import connect_to_mongo, connect_to_gridfs
from api.models import DocGeneralInfo , NlpAnalysis
from api.serializers import DocGeneralInfoSerializer, NlpAnalysisSerializer
def get_file_id_by_name(file_name):
    try:
        db = connect_to_mongo()
        file = db.fs.files.find_one({'filename': {'$regex': file_name, '$options': 'i'}})
        if file:
            return str(file['_id'])
        else:
            return None
    except errors.PyMongoError as e:
        return str(e)

def get_general_info_metadata(pdf_title):
    docs = DocGeneralInfo.objects.filter(title__icontains=pdf_title)
    serializer = DocGeneralInfoSerializer(docs, many=True)
    return serializer.data

def get_nlp_analysis_metadata(pdf_title):
    docs = NlpAnalysis.objects.filter(nlp_id__in=DocGeneralInfo.objects.filter(title__icontains=pdf_title).values_list('nlp_id', flat=True))
    serializer = NlpAnalysisSerializer(docs, many=True)
    return serializer.data


def get_text_from_pdf(file_id):
    try:
        fs = connect_to_gridfs()
        file = fs.get(ObjectId(file_id))
        doc = fitz.open(stream=file.read(), filetype="pdf")
        
        content = ""
        for page in doc:
            content += page.get_text()
        return content
    except Exception as e:
        return str(e)

def get_text_from_txt(file_id):
    try:
        fs = connect_to_gridfs()
        file = fs.get(ObjectId(file_id))
        content = file.read().decode('utf-8')
        return content
    except Exception as e:
        return str(e)
