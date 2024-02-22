from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from users.Authentication import UserAuthentication
from algolabs.config import get_user_from_token
from users.models import User

PISTON_SERVER_BASE_URL = "http://localhost:2000/api/v2/"


# @authentication_classes([UserAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_packages(request):
    packages_endpoint = PISTON_SERVER_BASE_URL + "packages"
    try:
        response = requests.get(packages_endpoint)
        return JsonResponse(response.json(), status=response.status_code, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500, safe=False)


# @authentication_classes([UserAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_runtimes(request):
    runtimes_endpoint = PISTON_SERVER_BASE_URL + "runtimes"
    try:
        response = requests.get(runtimes_endpoint)
        return JsonResponse(response.json(), status=response.status_code, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500, safe=False)


# @authentication_classes([UserAuthentication])
# @permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def install_package(request):
    packages_endpoint = PISTON_SERVER_BASE_URL + "packages"
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(packages_endpoint, data=request.body, headers=headers)
        if response.status_code == 200:
            return JsonResponse(response.json(), status=200, safe=False)
        else:
            return JsonResponse({"error": "Failed to process the request"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# @authentication_classes([UserAuthentication])
# @permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def uninstall_package(request):
    # user = get_user_from_token(request.headers)
    # if user.role != User.ADMIN:
    #     return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

    packages_endpoint = PISTON_SERVER_BASE_URL + "packages"
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(packages_endpoint, data=request.body, headers=headers)
        if response.status_code == 200:
            return JsonResponse(response.json(), status=200, safe=False)
        else:
            return JsonResponse({"error": "Failed to process the request"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def execute_code(request):
    execute_endpoint = PISTON_SERVER_BASE_URL + "execute"
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(execute_endpoint, data=request.body, headers=headers)
        if response.status_code == 200:
            return JsonResponse(response.json(), status=200, safe=False)
        else:
            return JsonResponse({"error": "Failed to process the request"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
