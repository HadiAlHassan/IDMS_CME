from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DocGeneralInfo
from .serializers import DocGeneralInfoSerializer
from datetime import datetime, timedelta

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