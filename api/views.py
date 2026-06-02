from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, StudentPerformanceLogSerializer
from .models import StudentPerformanceLog

from rest_framework.views import APIView
from .models import PlacementPrediction
from .serializers import PlacementPredictionSerializer

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


class PredictPlacementView(APIView):
    permission_classes = [IsAuthenticated] # Locked behind our secure JWT Bearer layer

    def post(self, request):
        user = request.user
        data = request.data

        try:
            cgpa = float(data.get('cgpa'))
            attendance = float(data.get('attendance_percentage'))
            backlogs = int(data.get('number_of_backlogs'))
            coding_rating = int(data.get('coding_rating'))
            
            if not (0.0 <= cgpa <= 10.0):
                return Response({"error": "CGPA values must be between 0.0 and 10.0."}, status=status.HTTP_400_BAD_REQUEST)
            if not (0.0 <= attendance <= 100.0):
                return Response({"error": "Attendance percentage must be between 0.0 and 100.0."}, status=status.HTTP_400_BAD_REQUEST)
            if backlogs < 0:
                return Response({"error": "Number of backlogs cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
            if not (1 <= coding_rating <= 5):
                return Response({"error": "Coding platform rating must be on a scale of 1 to 5."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid features data types provided. Ensure numeric formats."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Mock ML Pipeline Evaluation Algo
        base_score = (cgpa * 10) + (attendance * 0.2) + (coding_rating * 5)
        penalty = (backlogs * 15)
        computed_metric = base_score - penalty

        # Normalize score bounds cleanly into a probability percentage (0% to 100%)
        probability = max(0.0, min(100.0, round(computed_metric, 2)))

        # Classification boundary rules matching standard predictive outcomes
        if probability >= 60.0 and backlogs == 0:
            result = "Highly Likely to be Placed"
        elif probability >= 45.0 and backlogs <= 1:
            result = "Good Chance - Requires Skill Optimization"
        else:
            result = "At Academic Risk - Portfolio Improvement Needed"

        # 3. Restructure input values into an explicit JSON payload block
        input_payload = {
            "cgpa": cgpa,
            "attendance_percentage": attendance,
            "number_of_backlogs": backlogs,
            "coding_rating": coding_rating
        }

        # 4. Record and store the operational log persistently inside the database
        prediction_instance = PlacementPrediction.objects.create(
            student=user,
            input_features=input_payload,
            prediction_result=result,
            probability_score=probability
        )

        # 5. Serialize data state and dispatch response package
        serializer = PlacementPredictionSerializer(prediction_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PlacementPredictionHistoryView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user
        
        # Fetch all prediction records matching the current logged-in user
        predictions = PlacementPrediction.objects.filter(student=user).order_by('-predicted_at')
        
        # Serialize the query set (many=True handles a list of objects)
        serializer = PlacementPredictionSerializer(predictions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)