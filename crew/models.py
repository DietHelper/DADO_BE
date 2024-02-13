from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Crew(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, null=True)
    max_participants = models.IntegerField(default=0)
    
    STATUS_CHOICES = [
        ('종료', '종료'),
        ('모집중', '모집중'),
        ('진행중','진행중')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    is_active = models.BooleanField(default=True)
    participants = models.ManyToManyField(User, related_name='crew_participants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)