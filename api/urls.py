from django.urls import path
from .views import PredictPlacementView, RegisterView, StudentAcademicLogView, PlacementPredictionHistoryView

urlpatterns = [
    # 1. Signup Route
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    
    # 2. Dashboard Academic Metrics Route
    path('student/metrics/', StudentAcademicLogView.as_view(), name='student_metrics'),

    # 3. Core Placement Prediction Gateway Endpoint
    path('student/predict/', PredictPlacementView.as_view(), name='student_predict'),

    # 4. Placement History Log Retrieval Gateway
    path('student/predictions/history/', PlacementPredictionHistoryView.as_view(), name='prediction_history'),
]
