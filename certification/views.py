from authenticate.models import Student, University
from rest_framework import generics
from rest_framework.views import APIView, Response
from .serializers import (CertificateRequestSerializer, CertificateApproveSerializer,
                          CertificateDetailsSerializer, CertificateListSerializer,
                          CertificateVerificationSerializer)
from .helper_functions.pdf_helper import from_html
from .helper_functions.hash_helper import hash_from_file, from_file_object
from datetime import date
from certification_api.settings import contract_helper, firebase_storage
import os
from .helper_functions.email_helper import send_mail
from .models import Certificate
from django.contrib.auth.models import User

# Create your views here.


class CertificateRequest(APIView):
    serializer_class = CertificateRequestSerializer
    http_method_names = ['post']

    def post(self, request):
        result = 0
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = serializer.authenticate(token=serializer.data['token'])
        if not user:
            message = 'Authentication failed'
        else:
            certificate_id = serializer.request(
                validated_data=serializer.data, user=user)
            if certificate_id is None:
                message = 'University code does not exists'
            else:
                message = f'Request submitted successfully with ID {certificate_id}'
                result = 1
        return Response({
            'message': message,
            'result': result
        })


class CertificateApproval(APIView):
    serializer_class = CertificateApproveSerializer
    http_method_names = ['post']

    def post(self, request):
        result = 0
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = serializer.authenticate(token=serializer.data['token'])
        if not user:
            message = 'Authentication failed'
        else:
            certificate = serializer.is_authorized(
                serializer.data['certificate_id'], user)
            if not certificate:
                message = 'Authorization failed'
            else:
                certificate.certified_on = date.today()
                context = {
                    'certificate_id': certificate.certificate_id,
                    'student_name': certificate.student.name,
                    'course': certificate.course,
                    'university_name': certificate.university.name,
                    'generated_on': certificate.certified_on,
                    'grade_obtained': certificate.grade_obtained,
                    'email': certificate.student.user.email,
                }
                certificate_filename = from_html(context)
                file_hash = hash_from_file(certificate_filename)
                contract_helper.add_hash(certificate.certificate_id, file_hash)
                firebase_storage.child(f'{certificate.certificate_id}.pdf').put(
                    certificate_filename)
                url = firebase_storage.child(
                    f'{certificate.certificate_id}.pdf').get_url(None)
                certificate.certificate_link = url
                certificate.certified = True
                certificate.save()
                context['url'] = url
                send_mail(context)
                os.remove(certificate_filename)
                result = 1
                message = 'Certificate generated successfully'
        return Response({
            'message': message,
            'result': result
        })


class CertificateDetails(generics.ListAPIView):
    serializer_class = CertificateDetailsSerializer

    def get_queryset(self):
        certificate_id = self.request.query_params.get('certificate_id')
        if certificate_id is None:
            return None
        return Certificate.objects.filter(pk=certificate_id)


class CertificateListUniversity(generics.ListAPIView):
    serializer_class = CertificateListSerializer

    def get_queryset(self):
        university_code = self.request.query_params.get('university_code')
        try:
            certified = self.request.query_params.get(
                'certified').lower() == 'true'
        except AttributeError:
            certified = False
        if not university_code:
            return None
        try:
            user = User.objects.get(username=university_code)
            univeristy = University.objects.get(user=user)
        except (User.DoesNotExist, University.DoesNotExist):
            return None
        return Certificate.objects.filter(university=univeristy).filter(certified=certified)


class CertificateListStudent(generics.ListAPIView):
    serializer_class = CertificateListSerializer

    def get_queryset(self):
        username = self.request.query_params.get('student')
        try:
            certified = self.request.query_params.get(
                'certified').lower() == 'true'
        except AttributeError:
            certified = False
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            return None
        return Certificate.objects.filter(student=student).filter(certified=certified)


class CertificateVerification(APIView):
    serializer_class = CertificateVerificationSerializer

    def post(self, request):
        try:
            file = request.FILES.get('certificate', None)
            certificate_id = int(request.POST.get('certificate_id', None))
            if not file or not certificate_id:
                raise(ValueError)
            file_hash=from_file_object(file)
            validity=contract_helper.compare_hash(certificate_id, file_hash)
            if validity:
                message='The certificate is valid'
            else:
                message='The certificate is invalid'
            result=1
        except ValueError:
            result=0
            message='Invalid data recieved'
        return Response({
            'message': message,
            'result': result
        })

class CertificateDetailsStudent(generics.ListAPIView):
    serializer_class = CertificateDetailsSerializer

    def get_queryset(self):
        username = self.request.query_params.get('student')
        try:
            certified = self.request.query_params.get(
                'certified').lower() == 'true'
        except AttributeError:
            certified = False
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            return None
        return Certificate.objects.filter(student=student).filter(certified=certified)

class CertificateDetailsUniversity(generics.ListAPIView):
    serializer_class = CertificateDetailsSerializer

    def get_queryset(self):
        university_code = self.request.query_params.get('university_code')
        try:
            certified = self.request.query_params.get(
                'certified').lower() == 'true'
        except AttributeError:
            certified = False
        if not university_code:
            return None
        try:
            user = User.objects.get(username=university_code)
            univeristy = University.objects.get(user=user)
        except (User.DoesNotExist, University.DoesNotExist):
            return None
        return Certificate.objects.filter(university=univeristy).filter(certified=certified)
