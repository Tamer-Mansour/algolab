from django.urls import path

from content.views import *

urlpatterns = [
    path('', hello_world)
]