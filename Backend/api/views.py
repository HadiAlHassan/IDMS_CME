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
        db = connect_to_mongo()

        fs = GridFS(db)
        file_id = fs.put(pdf_file, filename=pdf_file.name)

        return Response({'message': 'PDF added successfully', 'file_id': str(file_id)})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
def get_pdf_by_id(request, file_id):
    try:
        db = connect_to_mongo()

        if not ObjectId.is_valid(file_id):
            return HttpResponse('Invalid file ID', status=400)
        
        fs = GridFS(db)
        
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except NoFile:
        return HttpResponse('File not found', status=404)
    except errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)

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

@api_view(['GET'])
def get_pdf_by_name(request, file_name):
    file_id = get_file_id_by_name(file_name)
    if file_id:
        return redirect('get_pdf_by_id', file_id=file_id)
    else:
        return HttpResponse('File not found', status=404)

@api_view(['GET'])
def list_files(request):
    try:
        db = connect_to_mongo()
        files_collection = db['fs.files']
        files = files_collection.find({}, {'filename': 1}) 
        file_list = [{'name': file['filename']} for file in files] 
        return JsonResponse({'files': file_list})
    except errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)   