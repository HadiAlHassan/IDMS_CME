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
# Create your views (endpoints) here.

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
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        fs = GridFS(db)

        # Save the file to GridFS
        file_id = fs.put(pdf_file, filename=pdf_file.name)

        return Response({'message': 'PDF added successfully', 'file_id': str(file_id)})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
# @api_view(['GET'])
# def get_pdf(request, file_id):
#     try:
#         # Connect to MongoDB
#         client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
#         db = client[settings.DATABASES['default']['NAME']]
#         fs = GridFS(db)

#         # Retrieve the file from GridFS
#         file = fs.get(file_id)

#         # Create a response with the PDF file
#         response = HttpResponse(file.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.filename)
#         return response
#     except Exception as e:
#         return HttpResponse(str(e), status=400)
# needs fixing !!!!!