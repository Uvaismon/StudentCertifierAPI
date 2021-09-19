from rest_framework import serializers
from django.contrib.auth.models import User
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
    