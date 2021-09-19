from authenticate.models import University
from django.urls import path
from .views import (RegisterStudent, Login, Logout,
                    RegisterUniversity)

urlpatterns = [
    path('register-student', RegisterStudent.as_view(), name='register_student'),
    path('login', Login.as_view(), name='login_student'),
    path('logout', Logout.as_view(), name='logout_student'),
    path('register-university', RegisterUniversity.as_view(),
         name='register_university'),
]
