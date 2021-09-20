from rest_framework import serializers
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView, Response
from django.db.utils import IntegrityError

from .serializers import (RegisterStudentSerializer, LoginSerializer, LogoutSerializer,
                          RegisterUniversitySerializer)


class RegisterStudent(APIView):
    serializer_class = RegisterStudentSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
            serializer.save()
            message = 'Account created successfully'
        except IntegrityError:
            message = 'Username already exists'
        return Response({
            'message': message
        })


class Login(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, user):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        token = serializer.get_token(serializer.data, user)
        if token is None:
            return Response({
                'token': 'Authentication failed'
            })
        return Response({
            'token': token
        })


class Logout(APIView):
    serializer_class = LogoutSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.delete_token(serializer.data)
        return Response({})


class RegisterUniversity(APIView):
    serializer_class = RegisterUniversitySerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
            serializer.save()
            message = 'Account created successfully'
        except IntegrityError:
            message = 'University code already exists'

        return Response({
            'message': message
        })
