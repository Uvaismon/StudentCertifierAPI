from logging import captureWarnings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from authenticate.models import Student, University
from .models import Certificate
from django.contrib.auth.models import User
from scaffolding.models import CourseDetails, COURSE_STATUS
from certification_api.settings import contract_helper

class CertificateRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    # university = serializers.CharField(max_length=64)
    # course = serializers.CharField(max_length=32)
    # grade_obtained = serializers.CharField(max_length=32)
    student_id = serializers.CharField(max_length=32)

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
            grade_obtained = validated_data['grade_obtained'],
            studentId = validated_data['student_id'],
            estimated_fee = contract_helper.estimate_fee_wei()
        )
        certificate.save()

        course_details = CourseDetails.objects.get(student_id=validated_data['student_id'])
        course_details.status = COURSE_STATUS[2]
        course_details.save()

        return certificate.certificate_id

class CertificateApproveSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    certificate_id = serializers.IntegerField()

    def authenticate(self, token):
        try:
            token = Token.objects.get(key=token)
            university = University.objects.get(user=token.user)
            return university
        except (Token.DoesNotExist, University.DoesNotExist):
            return None

    def is_authorized(self, certificate_id, user):
        try:
            certificate = Certificate.objects.get(certificate_id=certificate_id)
            if not certificate.university == user or certificate.certified:
                return None
            return certificate
        except Certificate.DoesNotExist:
            return None

class CertificateDetailsSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255)
    university = serializers.CharField(max_length=255)

    class Meta:
        model = Certificate
        fields = '__all__'

class CertificateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['certificate_id']

class CertificateVerificationSerializer(serializers.Serializer):
    certificate = serializers.FileField()
    certificate_id = serializers.IntegerField()

class CertificateRequestStudentSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    student_id = serializers.CharField(max_length=32)

class ConfirmEtherPaymentSerializer(serializers.Serializer):
    hash = serializers.CharField(max_length=128)
    certificate_id = serializers.IntegerField()
