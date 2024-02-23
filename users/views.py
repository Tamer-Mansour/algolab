import json
from algolabs.config import get_user_from_token
from django.contrib.auth.hashers import check_password
from rest_framework import views, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

from .Authentication import UserAuthentication
from .models import User
from .serializers import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserLoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_body = json.loads(request.body)
        email = request_body.get('email')
        password = request_body.get('password')
        user = User.objects.get(email=email)
        if user and check_password(password, user.password):
            refresh_token = RefreshToken.for_user(user=user)
            access_token = refresh_token.access_token
            return Response({'token': str(access_token), 'user_id': user.id, 'user_role': user.role}, status=status.HTTP_200_OK)
        return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            success_message = {"message": "User registered successfully"}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_users(request):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return Response({"error": "You are not authorized to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    all_users = [
        {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'avatar': user.avatar.url if user.avatar else None,
            'role': user.role,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }
        for user in users
    ]
    
    return Response(all_users, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        Session.objects.filter(session_key=request.session.session_key).delete()
        request.session.flush()
        logout(request)
        return response
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_users_by_role(request, role):
    try:
        user = get_user_from_token(request.headers)
        if user.role != User.ADMIN:
            return Response({"error": "You are not authorized to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        users = User.objects.filter(role=role)
        # Manually select the desired fields
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
            }
            for user in users
        ]
        return Response(users_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        
        # Extract only the allowed fields from request.data
        allowed_fields = ['first_name', 'last_name', 'email', 'role', 'date_of_birth', 'avatar', 'description', 'mobile', 'social_media_url', 'location']
        data_to_update = {field: request.data.get(field) for field in allowed_fields if field in request.data}
        
        serializer = UserSerializer(instance=user, data=data_to_update, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = get_user_from_token(request.headers)
        if user.role != User.ADMIN:
            return Response({"error": "You are not authorized to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(pk=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = get_user_from_token(request.headers)
        if user.role != User.ADMIN:
            return Response({"error": "You are not authorized to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(pk=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'date_of_birth': user.date_of_birth,
            'avatar': user.avatar.url,
            'description': user.description,
            'mobile': user.mobile,
            'social_media_url': user.social_media_url,
            'location': user.location,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
