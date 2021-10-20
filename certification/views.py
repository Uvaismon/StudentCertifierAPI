from re import A

from rest_framework.utils.serializer_helpers import ReturnList
from authenticate.models import Student, University
from rest_framework import generics, serializers
from rest_framework.views import APIView, Response

from certification.helper_functions.student_helper import verify_student
from .serializers import (CertificateRequestSerializer, CertificateApproveSerializer,
                          CertificateDetailsSerializer, CertificateListSerializer,
                          CertificateVerificationSerializer, CertificateRequestStudentSerializer,
                          ConfirmEtherPaymentSerializer)
from .helper_functions.pdf_helper import from_html
from .helper_functions.hash_helper import hash_from_file, from_file_object
from datetime import date
from certification_api.settings import contract_helper, firebase_storage, UNIVERSITY_CODE
import os
from .helper_functions.email_helper import send_mail
from .models import Certificate
from django.contrib.auth.models import User
from django.urls import reverse
from scaffolding.models import CourseDetails, COURSE_STATUS
from decouple import config

# Create your views here.


class CertificateRequest(APIView):
    serializer_class = CertificateRequestSerializer
    http_method_names = ['post']

    def post(self, request):
        print(request.data)
        result = 0
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = serializer.authenticate(token=serializer.data['token'])
        if not user:
            message = 'Authentication failed'
        # elif not verify_student(user.user.username, user.user.email, serializer.data['university']):
        #     message = 'Student does not belong to the mentioned univeristy'
        #     result = 2
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

                course_details = CourseDetails.objects.get(
                    student_id=certificate.studentId)
                course_details.status = COURSE_STATUS[3]
                course_details.save()

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
        return Certificate.objects.filter(university=univeristy).filter(certified=certified).filter(rejected=False).filter(payment_status=True)


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
        return Certificate.objects.filter(student=student).filter(certified=certified).filter(rejected=False).filter(payment_status=True)


class CertificateVerification(APIView):
    serializer_class = CertificateVerificationSerializer

    def post(self, request):
        try:
            file = request.FILES.get('certificate', None)
            certificate_id = int(request.POST.get('certificate_id', None))
            if not file or not certificate_id:
                raise(ValueError)
            file_hash = from_file_object(file)
            validity = contract_helper.compare_hash(certificate_id, file_hash)
            if validity:
                message = 'The certificate is valid'
            else:
                message = 'The certificate is invalid'
            result = 1
        except ValueError:
            result = 0
            message = 'Invalid data recieved'
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
        return Certificate.objects.filter(student=student).filter(certified=certified).filter(rejected=False).filter(payment_status=True)


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
        return Certificate.objects.filter(university=univeristy).filter(certified=certified).filter(rejected=False).filter(payment_status=True)


class EstimateFee(APIView):

    def get(self, request):
        usd = contract_helper.estimate_fee()
        usd = round(usd, 2)

        wei = contract_helper.estimate_fee_wei()
        ether = f'{wei / 10 ** 18 : .18f}'
        return Response({
            'USD': usd,
            'WEI': wei,
            'ETHER': ether
        })


class CertificateRequestStudent(APIView):
    serializer_class = CertificateRequestStudentSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        course_details = CourseDetails.objects.filter(
            student_id=serializer.data['student_id'])

        if not course_details:
            return Response({
                'result': 3,
                'message': 'Student is not enrolled into any course'
            })

        course_details = course_details[0]

        if course_details.status == COURSE_STATUS[0]:
            return Response({
                'result': 4,
                'message': 'Course incomplete',
            })

        if course_details.status == COURSE_STATUS[2]:
            return Response({
                'result': 5,
                'message': 'Already requested for the certificate'
            })

        if course_details.status == COURSE_STATUS[3]:
            return Response({
                'result': 6,
                'message': 'Already certified for the currently enrolled course'
            })

        _mutability = request.data._mutable
        request.data._mutable = True

        request.data['university'] = UNIVERSITY_CODE
        request.data['course'] = course_details.degree
        request.data['grade_obtained'] = course_details.grade

        request.data._mutable = _mutability

        certificate_view = CertificateRequest.as_view()
        return certificate_view(request._request, *args, **kwargs)


class CertificateLinkDeprecationMessage(APIView):

    def post(self, request):
        return Response(f'This link is deprecated. Please use the new link {reverse("certificate_request_student")}')

    def get(self, request):
        return self.post(request)


class RejectCertificate(APIView):
    serializer_class = CertificateApproveSerializer

    def post(self, request):
        result = 0

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = serializer.authenticate(token=serializer.data['token'])
        if not user:
            message = 'Authentication failed'
        else:
            certificate = serializer.is_authorized(
                serializer.data['certificate_id'], user
            )
            if not certificate:
                message = 'Authorization failed'
            else:
                certificate.rejected = True
                certificate.save()
                result = 1
                message = 'Certificate rejected successfully'

                course_details = CourseDetails.objects.get(
                    student_id=certificate.studentId)
                course_details.status = COURSE_STATUS[1]
                course_details.save()

        return Response({
            'result': result,
            'message': message
        })


class CertificateRejectionDetails(generics.ListAPIView):
    serializer_class = CertificateDetailsSerializer

    def get_queryset(self):
        username = self.request.query_params.get('student')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            return None
        return Certificate.objects.filter(student=student).filter(rejected=True)


class ConfirmEtherPayment(APIView):
    serializer_class = ConfirmEtherPaymentSerializer

    def post(self, request):
        result = 0
        message = 'Confirmation failed'
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
            certificate = Certificate.objects.get(
                certificate_id=serializer.data['certificate_id'])
            transaction_details = contract_helper.get_transaction_details(
                serializer.data['hash'])
            to = transaction_details['to']
            value = transaction_details['value']
            if (value >= certificate.estimated_fee and to == config('ETHEREUM_ACCOUNT_ADDRESS')
                    and Certificate.objects.filter(payment_details=serializer.data['hash']).count() == 0):
                result = 1
                certificate.payment_details = serializer.data['hash']
                certificate.payment_status = True
                certificate.save()
                message = 'Payment confirmed'

        except Certificate.DoesNotExist:
            message = 'certificate does not exist.'
        return Response({
            'result': result,
            'message': message
        })

class PendingPaymentDetails(generics.ListAPIView):
    serializer_class = CertificateDetailsSerializer

    def get_queryset(self):
        username = self.request.query_params.get('student')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            return None
        return Certificate.objects.filter(student=student).filter(payment_status=False)

class EthereumAccountAddress(APIView):

    def get(self, request):
        return Response({
            'account': config('ETHEREUM_ACCOUNT_ADDRESS')
        })