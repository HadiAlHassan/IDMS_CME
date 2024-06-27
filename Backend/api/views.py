from gridfs import GridFS, errors as gridfs_errors
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DocGeneralInfoSerializer


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
    
    