from rest_framework.serializers import Serializer
from rest_framework.views import APIView, Response
from .serializers import CertificateRequestSerializer

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
            certificate_id = serializer.request(validated_data=serializer.data, user=user)
            if certificate_id is None:
                message = 'University code does not exists'
            else:
                message = f'Request submitted successfully with ID {certificate_id}'
                result = 1
        return Response({
            'message': message,
            'result': result
        })