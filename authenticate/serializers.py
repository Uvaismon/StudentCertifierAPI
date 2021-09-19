from django.contrib import auth
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Student

class RegisterStudentSerializer(serializers.Serializer):
    usn = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=32)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            username=validated_data['usn'], 
            email=validated_data['email']
        )
        user.set_password(password)
        user.save()
        student = Student(
            name=validated_data['name'],
            user=user
        )
        student.save()
        return student

class LoginStudentSerializer(serializers.Serializer):
    usn = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)

    def get_token(self, validated_data):
        user = authenticate(username=validated_data['usn'], password=validated_data['password'])
        if not user:
            return None
        else:
            return str(Token.objects.get_or_create(user=user)[0])
