from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo.storage import GridFSStorage

# Create your models here.
# users_collection = db['users']

def user_avatar_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_avatars/<username>/<filename>
    return f'user_avatars/{instance.username}/{filename}'


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
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLES)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default='default_image.jpg', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    social_media_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.password.startswith('pbkdf2_sha256$'):
            # If it's a new user or the password is not hashed, hash it
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    