from django.db import models
from django.contrib.auth.models import User

# 1. Student Academic & Performance Logs Model
class StudentPerformanceLog(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="academic_logs")
    cgpa = models.FloatField(help_text="Current CGPA of the student")
    attendance_percentage = models.FloatField(help_text="Overall attendance percentage")
    number_of_backlogs = models.IntegerField(default=0, help_text="Number of active backlogs")
    coding_rating = models.IntegerField(help_text="Programming skill rating (1 to 5)")
    semester = models.IntegerField(help_text="Current Semester (1 to 8)")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - Sem {self.semester} Metrics"


# 2. Placement/Performance Prediction History Model
class PlacementPrediction(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    input_features = models.JSONField(help_text="The exact academic data JSON sent to the AIML model")
    prediction_result = models.CharField(max_length=255, help_text="Output prediction from the model")
    probability_score = models.FloatField(help_text="Confidence or probability percentage")
    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.student.username}: {self.prediction_result}"