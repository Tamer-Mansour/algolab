from django.http import HttpResponse, JsonResponse

from .config import get_user_from_token
from rest_framework.response import Response
from users.models import User
from rest_framework import status

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Code that is executed in each request before the view is called
        if 'login' in request.path or 'register' in request.path:
            response = self.get_response(request)
            return response
        user = get_user_from_token(request.headers)
        if type(user) == JsonResponse:
            return user

        if user.role != User.ADMIN:
            return JsonResponse({"error": "You are not authorized to perform this action."},status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        return response
