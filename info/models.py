from django.db import models
from django.contrib.auth.models import User
from django.db import models



class student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username



class notice(models.Model):
    text = models.TextField()
    file = models.FileField(upload_to='notices/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notice {self.id} @ {self.created_at:%Y-%m-%d %H:%M}"
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class chatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"
