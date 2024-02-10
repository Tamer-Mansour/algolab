from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


def get_user_from_token(header):
    if not header:
        return Response({'error': 'Authorization header not found.'}, status=status.HTTP_400_BAD_REQUEST)
    if not str(header['Authorization']).startswith('Bearer '):
        print(str(header))
        return Response({'error': 'Invalid Authorization header format.'}, status=status.HTTP_400_BAD_REQUEST)
    token = str(header['Authorization'])[len('Bearer '):]
    if not token:
        return Response({'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    access_token = AccessToken(token)
    user_id = access_token['user_id']
    user = User.objects.get(id=user_id)
    return user