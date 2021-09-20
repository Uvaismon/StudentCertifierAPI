from django.urls import path
from .views import CertificateRequest

urlpatterns = [
    path('certificate-request', CertificateRequest.as_view(), name='certificate_request'),
]
