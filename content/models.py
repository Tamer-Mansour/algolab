from django.db import models

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_challenges(self):
        return self.codingchallenge_set.all()

    def get_lessons(self):
        return self.lesson_set.all()

class Testcase(models.Model):
    name = models.CharField(max_length=255)
    input_value = models.TextField()
    expected_output = models.TextField()

class CodingChallenge(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    goal = models.TextField()
    description = models.TextField()
    constrains = models.TextField()
    code = models.TextField()
    function_signature = models.CharField(max_length=255)
    testcases = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
