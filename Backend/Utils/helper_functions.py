from pymongo import errors
from functools import wraps
import fitz
from bson import ObjectId

from Utils.db import connect_to_mongo, connect_to_gridfs
from api.models import DocGeneralInfo , NlpAnalysis
from api.serializers import DocGeneralInfoSerializer, NlpAnalysisSerializer
def get_file_id_by_name(file_name):
    try:
        print("Connecting to MongoDB...")
        db = connect_to_mongo()
        print("Connecting to GridFS...")
        fs = connect_to_gridfs()
        
        print(f"Searching for file with name: {file_name}")
        
        # Log all filenames in the database for debugging
        cursor = db.fs.files.find({})
        for document in cursor:
            print("Filename in DB:", document['filename'])
        
        # Use exact match instead of regex
        file = db.fs.files.find_one({'filename': file_name})
        
        if file:
            print(file["_id"])
            return str(file['_id'])
        else:
            print("File not found.")
            return None
    except errors.PyMongoError as e:
        print(f"PyMongoError: {str(e)}")
        return str(e)

def get_general_info_metadata(pdf_title):
    stripped_title = pdf_title.strip()
    print(f"Filtering DocGeneralInfo with title containing: {stripped_title}")
    
    # Fetch all documents and filter manually
    all_docs = DocGeneralInfo.objects.all()
    matching_docs = []
    for doc in all_docs:
        print(f"Title in DB: {doc.title}")
        if stripped_title.lower() in doc.title.lower():
            matching_docs.append(doc)
    
    print(f"Found {len(matching_docs)} DocGeneralInfo records for title: {stripped_title}")
    for doc in matching_docs:
        print(f"DocGeneralInfo title: {doc.title}, nlp_id: {doc.nlp_id}")
    
    serializer = DocGeneralInfoSerializer(matching_docs, many=True)
    return serializer.data

def get_nlp_analysis_metadata(pdf_title):
    stripped_title = pdf_title.strip()
    print(f"Filtering NlpAnalysis with related DocGeneralInfo titles containing: {stripped_title}")
    
    # Fetch all DocGeneralInfo documents and filter manually
    all_docs = DocGeneralInfo.objects.all()
    related_nlp_ids = []
    for doc in all_docs:
        print(f"Title in DB: {doc.title}")
        if stripped_title.lower() in doc.title.lower():
            related_nlp_ids.append(doc.nlp_id)
    
    print(f"Found related NLP IDs: {related_nlp_ids}")
    
    # Fetch NlpAnalysis documents using the related NLP IDs
    docs = NlpAnalysis.objects.filter(nlp_id__in=related_nlp_ids)
    print(f"Found {docs.count()} NlpAnalysis records for related NLP IDs")
    for doc in docs:
        print(f"NlpAnalysis nlp_id: {doc.nlp_id}, summary: {doc.summary}")
    
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
