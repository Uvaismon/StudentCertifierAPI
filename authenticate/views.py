from rest_framework.views import APIView, Response
from .serializers import RegisterStudentSerializer

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