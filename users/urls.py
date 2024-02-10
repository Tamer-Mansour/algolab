from django.urls import path

from . import views
from .views import UserLoginView, UserRegistrationView, get_users

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('get_users/', get_users, name='get_users')
]
