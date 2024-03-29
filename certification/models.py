from django.db import models
from django.db.models.fields.related import ForeignKey
from authenticate.models import Student, University

# Create your models here.

class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    student = ForeignKey(Student, on_delete=models.CASCADE)
    university = ForeignKey(University, on_delete=models.SET_NULL, null=True)
    studentId = models.CharField(max_length=32)
    course = models.CharField(max_length=32)
    grade_obtained = models.CharField(max_length=32)
    certified_on = models.DateField(null=True)
    certificate_link = models.CharField(max_length=128, null=True)
    certified = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    estimated_fee = models.BigIntegerField(null=True)
    payment_details = models.CharField(max_length=128, null=True)