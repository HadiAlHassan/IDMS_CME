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
from django.urls import reverse
from WebScraping.Scraper import Scraper


def connect_to_mongo():
    client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
    db = client[settings.DATABASES['default']['NAME']]
    return db

@api_view(['POST'])
def add_doc(request):
    try:
        serializer = DocGeneralInfoSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True) #based on the serializer class which is also based on the model class
        serializer.save()
        return True
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
        
        
        existing_file = fs.find_one({'filename': pdf_file.name})
        if existing_file:
            return Response({'error': 'File already exists'}, status=400)
        
        file_id = fs.put(pdf_file, filename=pdf_file.name)
        """
        Here I need to implement the code to save the file metadata in the database for now i will just save the file_id in the general info cluster
        """
        serializer = DocGeneralInfoSerializer(data={'source': 'PDF', 'title': pdf_file.name, 'author': 'Ahmad'})
        if serializer.is_valid():
            serializer.save()
            
            return Response({'message': 'PDF added successfully', 'file_id': str(file_id)})
        else:
            return Response({'error': 'Failed to add metadata and store the PDF', 'details': serializer.errors}, status=400)
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
def get_pdf_by_name(file_name):
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

@api_view(['POST'])
def handle_selected_pdfs(request):
    try:
        data=request.data
        selected_pdfs = data.get('selectedPdfs', [])
        if len(selected_pdfs) == 0:
            return Response({'message': 'No PDFs selected'}, status=200)
        
        pdf_file_ids = []
        for pdf_name in selected_pdfs:
            file_id = get_file_id_by_name(pdf_name)
            if file_id:
                pdf_file_ids.append(file_id)
            else:
                return Response({'error': f'File not found: {pdf_name}'}, status=404)
        
        pdf_urls = [request.build_absolute_uri(reverse('get_pdf_by_id', args=[file_id])) for file_id in pdf_file_ids]
        
        return Response({'message': 'PDFs found', 'pdfUrls': pdf_urls})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def view_docs(pdf_title):
    docs = DocGeneralInfo.objects.filter(title__icontains=pdf_title)
    serializer = DocGeneralInfoSerializer(docs, many=True)
    return serializer.data

@api_view(['POST'])
def get_metadata_by_pdf_name(request):
    try:
        data=request.data
        selected_pdfs = data.get('selectedPdfs')
        L =[]
        if len(selected_pdfs) == 0:
            return Response({'message': 'No PDFs '}, status=200)
        result_list = []
        for pdf_name in selected_pdfs:
            result_list.extend(view_docs(pdf_name))
        return Response({'message': 'PDFs found', 'pdf_metadata': result_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@api_view(['POST'])
def scrape_website(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'No URL provided'}, status=400)   
    try:
        scraper = Scraper()
        scraper.Scrape(url)
        return Response({'message': 'Website scraped successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
