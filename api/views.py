from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, StudentPerformanceLogSerializer
from .models import StudentPerformanceLog

# 1. Registration View 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# 2. Student Dashboard/Academic Log View 
class StudentAcademicLogView(generics.ListCreateAPIView):
    serializer_class = StudentPerformanceLogSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return StudentPerformanceLog.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)