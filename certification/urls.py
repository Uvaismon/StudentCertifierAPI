from django.urls import path
from .views import (CertificateApproval, CertificateDetails, RejectCertificate,
                    CertificateListUniversity, CertificateListStudent, CertificateVerification,
                    CertificateDetailsStudent, CertificateDetailsUniversity, EstimateFee,
                    CertificateRequestStudent, CertificateLinkDeprecationMessage,
                    CertificateRejectionDetails, ConfirmEtherPayment, PendingPaymentDetails)

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
    path('certificate-reject', RejectCertificate.as_view(),
         name='certificate_reject'),
    path('certificate-rejected', CertificateRejectionDetails.as_view(),
         name='certificate_rejected'),
     path('confirm-ether-payment', ConfirmEtherPayment.as_view(), name='confirm_ether_payment'),
     path('certificate-pending', PendingPaymentDetails.as_view(), name='certificate_pending')
]
