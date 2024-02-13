from rest_framework import serializers
from .models import *

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class CodingChallengeSerializer(serializers.ModelSerializer):
    chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all())

    class Meta:
        model = CodingChallenge
        fields = '__all__'