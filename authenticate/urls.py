from django.urls import path
from .views import RegisterStudent

urlpatterns = [
    path('register-student', RegisterStudent.as_view(), name='register_student'),
]