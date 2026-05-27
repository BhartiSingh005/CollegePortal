from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentPerformanceLog, PlacementPrediction

# 1. User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # Plain text password ko securely hash karke user create karein
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# 2. Academic Performance Serializer
class StudentPerformanceLogSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = StudentPerformanceLog
        fields = ['id', 'student_username', 'cgpa', 'attendance_percentage', 'number_of_backlogs', 'coding_rating', 'semester', 'updated_at']


# 3. Placement Prediction Logger Serializer
class PlacementPredictionSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = PlacementPrediction
        fields = ['id', 'student_username', 'input_features', 'prediction_result', 'probability_score', 'predicted_at']


