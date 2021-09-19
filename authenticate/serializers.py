from django.contrib import auth
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Student, University

class RegisterStudentSerializer(serializers.Serializer):
    Username = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=32)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            username=validated_data['Username'], 
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
    Username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)

    def get_token(self, validated_data):
        user = authenticate(username=validated_data['Username'], password=validated_data['password'])
        if not user:
            return None
        else:
            return str(Token.objects.get_or_create(user=user)[0])

class LogoutStudentSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)

    def delete_token(self, validated_data):
        try:
            token = Token.objects.get(key=validated_data['token'])
            token.delete()
        except Token.DoesNotExist:
            return

class RegisterUniversitySerializer(serializers.Serializer):
    university_code = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=32)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            username=validated_data['university_code'], 
            email=validated_data['email']
        )
        user.set_password(password)
        user.save()
        university = University(
            name=validated_data['name'],
            user=user
        )
        university.save()
        return university