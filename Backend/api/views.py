from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DocGeneralInfo
from .serializers import DocGeneralInfoSerializer
# Create your views (endpoints) here.

class DocGeneralInfoView(generics.ListAPIView):
    queryset = DocGeneralInfo.objects.all()
    serializer_class = DocGeneralInfoSerializer

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