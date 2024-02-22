from django.urls import path
from .views import *

urlpatterns = [
    path('solutions/', SolutionListCreateAPIView.as_view(), name='solution-list-create'),
    path('solutions/<int:pk>/', SolutionRetrieveUpdateDestroyAPIView.as_view(), name='solution-detail'),
    path('my-solutions/', StudentSolutionListAPIView.as_view(), name='student-solution-list'),
]
