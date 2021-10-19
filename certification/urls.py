from django.urls import path
from .views import (CertificateApproval, CertificateDetails,
                    CertificateListUniversity, CertificateListStudent, CertificateVerification,
                    CertificateDetailsStudent, CertificateDetailsUniversity, EstimateFee,
                    CertificateRequestStudent, CertificateLinkDeprecationMessage)

urlpatterns = [
    path('certificate-request', CertificateLinkDeprecationMessage.as_view(),
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
    path('certificate-details-list-student', CertificateDetailsStudent.as_view(),
         name='certificate_details_list_student'),
    path('certificate-details-list-university', CertificateDetailsUniversity.as_view(),
         name='certificate-details-list-university'),
    path('estimate-fee', EstimateFee.as_view(), name='estimate_fee'),
    path('certificate-request-student',
         CertificateRequestStudent.as_view(), name='certificate_request_student'),
]
