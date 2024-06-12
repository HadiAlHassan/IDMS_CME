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

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'This message is sent from the backend!'})