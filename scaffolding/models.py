from django.db import models
from django.db.models.fields import EmailField

# Create your models here.

class StudentDatabase(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    university = models.CharField(max_length=64)