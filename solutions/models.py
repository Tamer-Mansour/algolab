from django.db import models
from django.contrib.auth import get_user_model
from content.models import CodingChallenge
from users.models import User

User = get_user_model()


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(CodingChallenge, on_delete=models.CASCADE)
    answer = models.TextField()
    marks = models.PositiveIntegerField(null=True, blank=True)  # New field for marks
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
