from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import StudentDatabase, CourseDetails

# Register your models here.
admin.site.register(StudentDatabase)
admin.site.register(CourseDetails)