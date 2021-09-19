from django.urls import path
from .views import RegisterStudent, LoginStudent, LogoutStudent, Registeruniversity

urlpatterns = [
    path('register-student', RegisterStudent.as_view(), name='register_student'),
    path('login-student', LoginStudent.as_view(), name='login_student'),
    path('logout-student', LogoutStudent.as_view(), name='logout_student'),

    path('register-university', Registeruniversity.as_view(), name='register_university'),
]