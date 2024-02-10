import json
from algolabs.config import get_user_from_token
from django.contrib.auth.hashers import check_password
from rest_framework import views, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

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
            return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
        return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_users(request):
    user = get_user_from_token(request.headers)
    if user.role == User.ADMIN:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
