from django.urls import path
from .views import *

urlpatterns = [
    path('packages', get_available_packages),
    path('packages/install', install_package),
    path('packages/delete', uninstall_package),
    path('runtimes', get_runtimes),
    path('execute', execute_code),
]
