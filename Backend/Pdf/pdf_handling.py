from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from pymongo import errors as pymongo_errors
from django.db import transaction
import datetime 

from Utils.db import connect_to_mongo, connect_to_gridfs
from Utils.helper_functions import get_file_id_by_name, get_metadata, get_text_from_pdf
from api.serializers import DocGeneralInfoSerializer, NlpAnalysisSerializer
from Utils.decorators import timing_decorator

@timing_decorator
@api_view(['POST'])
def add_pdf(request):
    try:
        pdf_file = request.FILES.get('file')
        if not pdf_file:
            return Response({'error': 'No PDF file provided'}, status=400)
        
        if not pdf_file.name.endswith('.pdf'):
            return Response({'error': 'Invalid file type'}, status=400)
        fs = connect_to_gridfs()
              
        existing_file = fs.find_one({'filename': pdf_file.name})
        if existing_file:
            return Response({'error': 'File already exists'}, status=400)
        
        file_id = fs.put(pdf_file, filename=pdf_file.name)
        """
        Here I need to implement the code to save the file metadata in the database for now i will just save the file_id in the general info cluster
        """
        with transaction.atomic():
            # Save DocGeneralInfo
            general_info_data = {
                'source': 'PDF',
                'title': pdf_file.name,
                'author': 'Ahmad'
            }
            general_info_serializer = DocGeneralInfoSerializer(data=general_info_data)
            if general_info_serializer.is_valid():
                general_info = general_info_serializer.save()
            else:
                return Response({'error': 'Failed to add DocGeneralInfo', 'details': general_info_serializer.errors}, status=400)
            
            # Save NlpAnalysis
            nlp_analysis_data = {
                'nlp_id': general_info.nlp_id,
                'document_type': 'PDF',
                'keywords': [],  # Add your keyword extraction logic here
                'summary': '',  # Add your summarization logic here
                'document_date': datetime.now().date(),
                'category': 'Legal',  # Example category, change as needed
                'related_documents': [],
                'language': 'English',  # Example language, change as needed
                'version': '1.0',  # Example version, change as needed
                'confidentiality_level': 'Public',  # Example confidentiality level, change as needed
                'location': 'Location A',  # Example location, change as needed
                'references': [],
                'uploaded_by': 'Ahmad',  # Example uploader, change as needed
                'related_projects': []
            }
            nlp_analysis_serializer = NlpAnalysisSerializer(data=nlp_analysis_data)
            if nlp_analysis_serializer.is_valid():
                nlp_analysis_serializer.save()
            else:
                return Response({'error': 'Failed to add NlpAnalysis', 'details': nlp_analysis_serializer.errors}, status=400)
        
        return Response({'message': 'PDF, metadata, and NLP_analysis added successfully', 'file_id': str(file_id)})
    except pymongo_errors.PyMongoError as e:
        return Response({'error': str(e)}, status=400)

@timing_decorator 
@api_view(['GET'])
def get_pdf_by_id(request, file_id):
    try:
        if not ObjectId.is_valid(file_id):
            return HttpResponse('Invalid file ID', status=400)
        fs = connect_to_gridfs()
        
        file = fs.get(ObjectId(file_id))  # Corrected "Objectid" to "ObjectId"
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except pymongo_errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)

@timing_decorator
@api_view(['GET'])
def get_pdf_by_name(request, file_name):
    file_id = get_file_id_by_name(file_name)
    if file_id:
        return redirect('get_pdf_by_id', file_id=file_id)
    else:
        return HttpResponse('File not found', status=404)

@timing_decorator
@api_view(['GET', 'POST'])
def list_pdfs(request):
    try:
        db = connect_to_mongo()
        files_collection = db['general_info']
        files = files_collection.find({}, {'title': 1, 'source': 1})  # Include 'source' in the projection
        file_list = [{'name': file['title']} for file in files if file['source'] == "PDF"]
        return JsonResponse({'files': file_list})
    except pymongo_errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)   

@timing_decorator     
@api_view(['POST'])
def handle_selected_pdfs(request):
    try:
        data = request.data
        if data is None:
            return Response({'error': 'Request data is missing'}, status=400)
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
        
        return Response({'message': 'PDFs found', 'pdfUrls': pdf_urls})  # Corrected this line by adding the missing parenthesis
    except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

@timing_decorator
@api_view(['POST'])
def get_metadata_by_pdf_name(request):
    try:
        data = request.data
        selected_pdfs = data.get('selectedPdfs')

        if len(selected_pdfs) == 0:
            return Response({'message': 'No PDFs selected'}, status=200)  

        metadata_list = []
        for pdf_name in selected_pdfs:
            metadata_list.extend(get_metadata(pdf_name))
        return Response({'message': 'PDFs found', 'pdf_metadata': metadata_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)