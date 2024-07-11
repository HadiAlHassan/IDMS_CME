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
def update_case(request):
    try:
        # Extract data from request
        name = request.data.get('name')
        user_id = request.data.get('user_id')
        
        # Ensure the essential fields are provided
        if not all([name, user_id]):
            return Response({'error': 'Name and user_id are required'}, status=400)
        
        # Fields to update
        new_name = request.data.get('new_name')
        client = request.data.get('client')
        status = request.data.get('status')
        time = request.data.get('time')
        trial_date = request.data.get('trial_date')
        document_titles = request.data.get('document_titles', [])
        # Connect to MongoDB
        db = connect_to_mongo()

        # Find the case by name and user_id
        existing_case = db.cases.find_one({'name': name, 'user_id': user_id})
        if not existing_case:
            return Response({'error': 'Case not found'}, status=404)

        # Update fields
        update_fields = {}
        if new_name:
            update_fields['name'] = new_name
        if client:
            update_fields['client'] = client
        if status:
            update_fields['status'] = status
        if time:
            update_fields['time'] = time
        if trial_date:
            update_fields['trial_date'] = trial_date
        if document_titles:
            update_fields['documents_related'] = document_titles
        if update_fields:
            db.cases.update_one({'name': name, 'user_id': user_id}, {'$set': update_fields})

        return Response({'message': 'Case updated successfully'}, status=200)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)

@timing_decorator
@api_view(['POST'])
def get_cases_by_user(request):
    try:
        # Extract the user_id from the request body
        user_id = request.data.get('user_id')
 
        # Validate required field
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
 
        # Connect to MongoDB
        db = connect_to_mongo()
 
        # Check if the user exists by querying the user collection
        user_exists = db.user.find_one({'firebase_uid': user_id})
        if not user_exists:
            return Response({'error': 'User does not exist'}, status=404)
 
        # Retrieve all cases for the given user_id
        cases = db.cases.find({'user_id': user_id})
 
        # Convert cases to a list of dictionaries
        case_list = []
        for case in cases:
            case_list.append({
                'name': case.get('name'),
                'client': case.get('client'),
                'status': case.get('status'),
                'time': case.get('time'),
                'documents_related': case.get('documents_related'),
                'trial_date': case.get('trial_date'),
                'user_id': case.get('user_id')
            })
 
        return Response({'cases': case_list}, status=200)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)
    
@timing_decorator
@api_view(['POST'])
def get_case_details(request):
    try:
        # Extract case data from request body
        case_name = request.data.get('name', '').strip()
        user_id = request.data.get('user_id', '').strip()

        # Log the received values
        logger.info(f"Received request for case: '{case_name}' and user: '{user_id}'")

        # Validate required fields
        if not all([case_name, user_id]):
            logger.error('Missing required fields in request')
            return Response({'error': 'name and user_id are required'}, status=400)

        # Connect to MongoDB
        db = connect_to_mongo()

        # Check if the user exists
        user_exists = db.user.find_one({'firebase_uid': user_id})
        if not user_exists:
            logger.error(f'User with ID {user_id} does not exist')
            return Response({'error': 'User does not exist'}, status=404)

        # Check if the case exists for the given user_id
        case = db.cases.find_one({'name': case_name, 'user_id': user_id}, {'_id': 0})
        if not case:
            logger.error(f'Case {case_name} not found for user {user_id}')
            return Response({'error': 'Case not found for this user'}, status=404)

        # Return case information
        return Response({
            'name': case.get('name'),
            'client': case.get('client'),
            'status': case.get('status'),
            'time': case.get('time'),
            'documents_related': case.get('documents_related'),
            'trial_date': case.get('trial_date'),
            'user_id': case.get('user_id')
        }, status=200)

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
    

from datetime import datetime

 
@api_view(['POST'])
def get_upcoming_trials(request):
    try:
        # Extract user_id from request
        user_id = request.data.get('user_id')
        
        # Validate required field
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        # Connect to MongoDB
        db = connect_to_mongo()
        
        # Check if the user exists in the user collection
        user_exists = db.user.find_one({'firebase_uid': user_id})
        if not user_exists:
            return Response({'error': 'User does not exist'}, status=404)
        
        # Retrieve all cases for the given user_id with trial dates after today
        today = datetime.utcnow().strftime('%Y-%m-%d')
        cases = db.cases.find({'user_id': user_id, 'trial_date': {'$gt': today}})
        
        # Convert cases to a list of dictionaries
        upcoming_trials = []
        for case in cases:
            upcoming_trials.append({
                'caseId': str(case.get('_id')),  # Ensure caseId is a string
                'caseName': case.get('name'),
                'date': case.get('trial_date')
            })
        
        upcoming_trials = sorted(upcoming_trials, key=lambda x: x['date'])
        return Response({'upcoming_trials': upcoming_trials}, status=200)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return Response({'error': 'An unexpected error occurred'}, status=500)
    
@timing_decorator
@api_view(['GET'])
def get_case_counts(request):
    try:
        # Connect to MongoDB
        db = connect_to_mongo()
 
        # Count cases by their status
        open_count = db.cases.count_documents({'status': 'Open'})
        closed_count = db.cases.count_documents({'status': 'Closed'})
        pending_count = db.cases.count_documents({'status': 'Pending'})
 
        return Response({
            'Open': open_count,
            'Closed': closed_count,
            'Pending': pending_count
        }, status=200)
 
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'An unexpected error occurred'}, status=500)