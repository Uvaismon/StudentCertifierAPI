from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView, Response
from .serializers import RegisterStudentSerializer, LoginStudentSerializer

# Create your views here.

class RegisterStudent(APIView):
    serializer_class = RegisterStudentSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({
            'message': "Account created successfully"
        })

class LoginStudent(APIView):
    serializer_class = LoginStudentSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        token = serializer.get_token(serializer.data)
        if token is None:
            return Response({
                'token': 'Authentication failed'
            })
        return Response({
            'token': token
        })
