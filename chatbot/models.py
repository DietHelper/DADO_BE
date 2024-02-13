from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)