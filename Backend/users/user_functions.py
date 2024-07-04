import pyrebase

# Firebase configuration
from .firebase_config import firebaseConfig
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer
from api.models import User
from Utils.decorators import timing_decorator
from rest_framework.decorators import api_view
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@timing_decorator
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        firebase_uid = user['localId']
        
        # Check if the user exists in the Django backend
        try:
            django_user = User.objects.get(email=email)
            if django_user.firebase_uid == firebase_uid:
                return Response({"message": "Successfully logged in!", "user": user}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User ID mismatch."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User does not exist in the Django backend."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "Invalid email or password.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@timing_decorator
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            # Save the user in the Django database with hashed password
            django_user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                firebase_uid=user['localId']
            )
            return Response({"message": "Successfully created an account!", "user": user}, status=status.HTTP_201_CREATED)
        except auth.EmailAlreadyExistsError:
            return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)