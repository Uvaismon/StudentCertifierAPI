from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=64)
    user = OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class University(models.Model):
    name = models.CharField(max_length=64)
    user = OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
