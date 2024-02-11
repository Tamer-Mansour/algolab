from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('logout/', logout_user, name='user-logout'),
    path('get_users/', get_users, name='get_users'),
    path('get_users_by_role/<str:role>', get_users_by_role, name='get_users_by_role'),
    path('user/update/<int:user_id>/', update_user, name='update-user'),
    path('user/delete/<int:user_id>/', delete_user, name='delete-user'),
]
