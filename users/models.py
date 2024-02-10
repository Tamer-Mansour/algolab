from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# users_collection = db['users']


class User(AbstractUser):
    ROLES = (
        ('student', 'STUDENT'),
        ('admin', 'ADMIN'),
        ('instructor', 'INSTRUCTOR'),
    )
    STUDENT = 'student'
    ADMIN = 'admin'
    INSTRUCTOR = 'instructor'
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
