import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Case
from Utils.db import connect_to_mongo
from Utils.decorators import timing_decorator
import uuid
logger = logging.getLogger(__name__)
 
@timing_decorator
@api_view(['POST'])
def create_case(request):
    try:
        # Extract case data from request
        name = request.data.get('name')
        client = request.data.get('client')
        status = request.data.get('status')
        time = request.data.get('time')
        trial_date = request.data.get('trial_date')
        user_id = request.data.get('user_id')
 
        # Validate required fields
        if not all([name, client, status, time, trial_date, user_id]):
            return Response({'error': 'All fields are required'}, status=400)
 
        # Connect to MongoDB
        db = connect_to_mongo()
 
        # Check for duplicate case name
        existing_case = db.cases.find_one({'name': name, 'user_id': user_id})
        if existing_case:
            return Response({'error': 'A case with this name already exists for this user'}, status=400)
 
        # Create and save the case
        new_case = {
            
            'name': name,
            'client': client,
            'status': status,
            'time': time,
            'documents_related': [],
            'trial_date': trial_date,
            'user_id': user_id
        }
        result = db.cases.insert_one(new_case)  # Save the new case to the 'cases' collection
 
        return Response({'message': 'Case created successfully', 'case_id': str(result.inserted_id)}, status=201)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)
   
 
from api.models import DocGeneralInfo
@timing_decorator
@api_view(['PUT'])
def update_case_status(request):
    try:
        # Extract case data from request
        name = request.data.get('name')
        new_status = request.data.get('status')
        user_id = request.data.get('user_id')
        
        # Validate required fields
        if not all([name, new_status, user_id]):
            return Response({'error': 'Name and status are required'}, status=400)
 
        # Connect to MongoDB
        db = connect_to_mongo()
 
        # Find the case by name
        existing_case = db.cases.find_one({'name': name, 'user_id': user_id})
        if not existing_case:   
            return Response({'error': 'Case not found'}, status=404)
 
        # Update the case status
        db.cases.update_one({'name': name}, {'$set': {'status': new_status}})
 
        return Response({'message': 'Case status updated successfully'}, status=200)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)
   
 
@timing_decorator
@api_view(['PUT'])
def add_documents_to_case(request):
    try:
        # Extract case data from request
        name = request.data.get('name')
        document_titles = request.data.get('document_titles', [])
        user_id = request.data.get('user_id')
 
        # Validate required fields
        if not all([name, document_titles, user_id]):
            return Response({'error': 'Name, document_titles, and user_id are required'}, status=400)
 
        # Connect to MongoDB
        db = connect_to_mongo()
 
        # Find the case by name and user_id
        existing_case = db.cases.find_one({'name': name, 'user_id': user_id})
        if not existing_case:
            return Response({'error': 'Case not found for this user'}, status=404)
 
        # Retrieve documents from the DocGeneralInfo collection
        documents = []
        for title in document_titles:
            doc_info = DocGeneralInfo.objects.filter(title=title).first()
            if doc_info:
                documents.append(title)
 
        if not documents:
            return Response({'error': 'No valid documents found'}, status=400)
 
        # Add documents to the case
        db.cases.update_one({'name': name, 'user_id': user_id}, {'$addToSet': {'documents_related': {'$each': documents}}})
 
        return Response({'message': 'Documents added successfully'}, status=200)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)
 
   
@timing_decorator
@api_view(['GET'])
def get_all_titles(request):
    try:
        # Retrieve all titles from the DocGeneralInfo collection
        titles = DocGeneralInfo.objects.values_list('title', flat=True)
       
        return Response({'titles': list(titles)}, status=200)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)