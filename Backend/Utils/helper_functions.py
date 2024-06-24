from pymongo import errors
from functools import wraps
from Utils.db import connect_to_mongo
from api.models import DocGeneralInfo
from api.serializers import DocGeneralInfoSerializer

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

def get_metadata(pdf_title):
    docs = DocGeneralInfo.objects.filter(title__icontains=pdf_title)
    serializer = DocGeneralInfoSerializer(docs, many=True)
    return serializer.data

def mongo_connection(func):
    def wrapper(request, *args, **kwargs):
        db = connect_to_mongo()
        return func(request, db, *args, **kwargs) 
    return wrapper