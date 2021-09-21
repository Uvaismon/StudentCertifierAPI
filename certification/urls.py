from django.urls import path
from .views import (CertificateRequest, CertificateApproval, CertificateDetails,
                    CertificateListUniversity, CertificateListStudent, CertificateVerification)

urlpatterns = [
    path('certificate-request', CertificateRequest.as_view(),
         name='certificate_request'),
    path('certificate-approve', CertificateApproval.as_view(),
         name='certificate_approve'),
    path('certificate-details', CertificateDetails.as_view(),
         name='certificate_details'),
    path('certificate-list-university', CertificateListUniversity.as_view(),
         name='certificate_list_univeristy'),
    path('certificate-list-student', CertificateListStudent.as_view(),
         name='certificate_list_student'),
    path('certificate-verification', CertificateVerification.as_view(),
         name='certificate_verification'),
]
