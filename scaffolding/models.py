from django.db import models
from django.db.models.fields import EmailField

# Create your models here.

COURSE_STATUS = ('INCOMPLETE', 'COMPLETE', 'REQUESTED', 'CERTIFIED')

class StudentDatabase(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    university = models.CharField(max_length=64)

class CourseDetails(models.Model):
    student_id = models.CharField(max_length=32, primary_key=True)
    degree = models.CharField(max_length=32)
    grade = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default=COURSE_STATUS[0])