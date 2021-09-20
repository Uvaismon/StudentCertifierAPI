from django.urls import path
from .views import CertificateRequest, CertificateApproval

urlpatterns = [
    path('certificate-request', CertificateRequest.as_view(), name='certificate_request'),
    path('certificate-approve', CertificateApproval.as_view(), name='certificate_approve'),
]
