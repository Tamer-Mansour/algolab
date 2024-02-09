from django.http import HttpResponse
from django.shortcuts import render
from .models import users_collection
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the")


def get_all_users(request):
    users = users_collection.objects.find()
    return HttpResponse(users)