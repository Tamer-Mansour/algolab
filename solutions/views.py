from django.http import JsonResponse
from rest_framework import generics, permissions, status
from .models import Solution
from .serializers import SolutionSerializer
from users.models import User
from algolabs.config import get_user_from_token

class IsStudentOrInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_user_from_token(request.headers)
        return user.role in ['student', 'instructor']

class SolutionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrInstructor]

    def perform_create(self, serializer):
        user = get_user_from_token(self.request.headers)
        serializer.save(user=user)
        return JsonResponse({"message": "Solution created successfully"}, status=status.HTTP_201_CREATED)

class SolutionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrInstructor]

    def perform_update(self, serializer):
        serializer.save()
        return JsonResponse({"message": "Solution updated successfully"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return JsonResponse({"message": "Solution deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class StudentSolutionListAPIView(generics.ListAPIView):
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_user_from_token(self.request.headers)
        return Solution.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse({"message": "List of student solutions", "data": serializer.data}, status=status.HTTP_200_OK)
