from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DocGeneralInfo
from .serializers import DocGeneralInfoSerializer
from datetime import datetime, timedelta
from pymongo import MongoClient
from gridfs import GridFS
from django.conf import settings
from bson.objectid import ObjectId
from gridfs.errors import NoFile
from pymongo import errors
from django.shortcuts import redirect
from django.http import JsonResponse


def connect_to_mongo():
    client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
    db = client[settings.DATABASES['default']['NAME']]
    return db

@api_view(['GET'])
def view_docs(request):
    try:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date:
            start_date = datetime.now() - timedelta(weeks=2)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if not end_date:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        docs = DocGeneralInfo.objects.filter(date_submitted__gte=start_date, date_submitted__lt=end_date)
        serializer = DocGeneralInfoSerializer(docs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def add_doc(request):
    try:
        serializer = DocGeneralInfoSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True) #based on the serializer class which is also based on the model class
        serializer.save()
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)})
    

@api_view(['POST'])
def add_pdf(request):
    try:
        pdf_file = request.FILES.get('file')
        if not pdf_file:
            return Response({'error': 'No PDF file provided'}, status=400)

        # Connect to MongoDB
        db = connect_to_mongo()

        # Save the file to GridFS
        file_id = db.put(pdf_file, filename=pdf_file.name)

        return Response({'message': 'PDF added successfully', 'file_id': str(file_id)})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
def get_pdf_by_id(request, file_id):
    try:
        # Connect to MongoDB
        db = connect_to_mongo()

        # Ensure the file_id is a valid ObjectId
        if not ObjectId.is_valid(file_id):
            return HttpResponse('Invalid file ID', status=400)
        
        fs = GridFS(db)
        # Retrieve the file from GridFS
        file = fs.get(ObjectId(file_id))

        # Create a response with the PDF file
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except NoFile:
        return HttpResponse('File not found', status=404)
    except errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)

def get_file_id_by_name(file_name):
    try:
        # Connect to MongoDB
        db = connect_to_mongo()

        # Query the file by name
        file = db.fs.files.find_one({'filename': {'$regex': file_name, '$options': 'i'}})
        if file:
            return str(file['_id'])
        else:
            return None
    except errors.PyMongoError as e:
        return str(e)

@api_view(['GET'])
def get_pdf_by_name(request, file_name):
    # Use the existing function to get the file ID by name
    file_id = get_file_id_by_name(file_name)
    
    if file_id:
        # Redirect to the get_pdf view if the file ID was found
        return redirect('get_pdf_by_id', file_id=file_id)
    else:
        # Return an error response if the file was not found
        return HttpResponse('File not found', status=404)

@api_view(['GET'])
def list_files(request):
    try:
        db = connect_to_mongo()
        # Assuming your files are stored in a collection named 'fs.files'
        files_collection = db['fs.files']
        files = files_collection.find({}, {'_id': 1, 'filename': 1})  # Fetch only the _id and filename fields
        file_list = [{'name': file['filename'], 'id': str(file['_id'])} for file in files]
        return JsonResponse({'files': file_list})
    except errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)   