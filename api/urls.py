from django.urls import path
from .views import RegisterView, StudentAcademicLogView

urlpatterns = [
    # 1. Signup Route
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    
    # 2. Dashboard Academic Metrics Route
    path('student/metrics/', StudentAcademicLogView.as_view(), name='student_metrics'),
]
