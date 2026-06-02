from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_api_exception_handler(exc, context):
    
    response = exception_handler(exc, context)


    if response is None:
        return Response({
            "error": "A critical system error occurred on the server. Engineering has been notified.",
            "details": str(exc) if hasattr(exc, 'message') else "Internal Server Error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.data = {
        "error": "Request validation or security clearance failed.",
        "messages": response.data
    }

    return response