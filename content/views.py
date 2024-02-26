from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework import views, status
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.Authentication import UserAuthentication
from algolabs.config import get_user_from_token
from users.models import User
from django.shortcuts import get_object_or_404



@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
# @permission_classes([AllowAny])
def add_chapter(request):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        if request.method == 'POST':
            title = request.data.get('title')

            # Check if a chapter with the provided title already exists
            existing_chapter = Chapter.objects.filter(title=title).first()
            if existing_chapter:
                return Response({'error': f'Chapter with title "{title}" already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = ChapterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
def get_chapters(request):
    try:
        if request.method == 'GET':
            chapters = Chapter.objects.all()
            serializer = ChapterSerializer(chapters, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
def list_chapters_with_details(request):
    chapters = Chapter.objects.all()
    serialized_data = []
    for chapter in chapters:
        chapter_data = ChapterSerializer(chapter).data
        # chapter_data['lessons'] = LessonSerializer(chapter.get_lessons(), many=True).data
        chapter_data['challenges'] = CodingChallengeSerializer(chapter.get_challenges(), many=True).data
        serialized_data.append(chapter_data)
    return Response(serialized_data)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
def get_chapter_with_challenges_by_id(request, chapter_id):
    try:
        chapter = Chapter.objects.prefetch_related('codingchallenge_set').get(pk=chapter_id)
        chapter_data = ChapterSerializer(chapter).data
        coding_challenges_data = CodingChallengeSerializer(chapter.codingchallenge_set.all(), many=True).data
        chapter_data['challenges'] = coding_challenges_data
        return Response(chapter_data)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
# @authentication_classes([UserAuthentication])
# @permission_classes([IsAuthenticated])
def get_chapter_by_id(request, chapter_id):
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
# @permission_classes([AllowAny])
def edit_chapter(request, chapter_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
        if request.method == 'PUT':
            serializer = ChapterSerializer(chapter, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
# @permission_classes([AllowAny])
def delete_chapter(request, chapter_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
        if request.method == 'DELETE':
            chapter.delete()
            return Response({'message': 'Chapter deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
# @permission_classes([AllowAny])
def add_coding_challenge(request):
    try:
        user = get_user_from_token(request.headers)
        if user.role != User.ADMIN:
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
        if request.method == 'POST':
            serializer = CodingChallengeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If serializer is not valid, return detailed validation errors
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
def get_coding_challenges(request):
    try:
        if request.method == 'GET':
            coding_challenges = CodingChallenge.objects.all()
            serializer = CodingChallengeSerializer(coding_challenges, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
# @permission_classes([AllowAny])
def get_coding_challenge_by_id(request, challenge_id):
    try:
        coding_challenge = CodingChallenge.objects.get(pk=challenge_id)
        serializer = CodingChallengeSerializer(coding_challenge)
        return Response(serializer.data)
    except CodingChallenge.DoesNotExist:
        return Response({'error': 'Coding challenge not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
# @permission_classes([AllowAny])
def edit_coding_challenge(request, challenge_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        coding_challenge = CodingChallenge.objects.get(pk=challenge_id)
        if request.method == 'PUT':
            serializer = CodingChallengeSerializer(coding_challenge, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    except CodingChallenge.DoesNotExist:
        return Response({'error': 'Coding challenge not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_coding_challenge(request, challenge_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        coding_challenge = CodingChallenge.objects.get(pk=challenge_id)
        if request.method == 'DELETE':
            coding_challenge.delete()
            return Response({'message': 'Coding challenge deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except CodingChallenge.DoesNotExist:
        return Response({'error': 'Coding challenge not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_course(request):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        if request.method == 'POST':
            serializer = CourseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_course(request, course_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(instance=course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_course(request, course_id):
    user = get_user_from_token(request.headers)
    if user.role != User.ADMIN:
        return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)
    try:
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_courses(request):
    try:
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_course_by_id(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)