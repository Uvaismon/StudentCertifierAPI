from rest_framework import serializers
from rest_framework.authtoken.models import Token
from authenticate.models import Student, University
from .models import Certificate
from django.contrib.auth.models import User

class CertificateRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    university = serializers.CharField(max_length=64)
    course = serializers.CharField(max_length=32)
    grade_obtained = serializers.CharField(max_length=3)

    def authenticate(self, token):
        try:
            token = Token.objects.get(key=token)
            student = Student.objects.get(user=token.user)
            return student
        except (Student.DoesNotExist, Token.DoesNotExist):
            return None

    def request(self, validated_data, user):
        try:
            user_univ = User.objects.get(username=validated_data['university'])
            university = University.objects.get(user=user_univ)
        except (University.DoesNotExist, User.DoesNotExist):
            return None
        certificate = Certificate(
            student = user,
            university = university,
            course = validated_data['course'],
            grade_obtained = validated_data['grade_obtained']
        )
        certificate.save()
        return certificate.certificate_id