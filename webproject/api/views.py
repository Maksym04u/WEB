# views.py
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .tasks import generate_chart
from rest_framework.permissions import IsAuthenticated
from .models import History
from .serializers import HistorySerializer  # Add this serializer

from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from celery.exceptions import Ignore


class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Please provide both username and password."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create_user(username=username, password=password)

        # Authenticate user after creation
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Create response with token in the cookie
            response = Response({
                'message': 'Registration successful',
            }, status=status.HTTP_201_CREATED)

            # Set token in the cookie
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,  # Prevent JS access to the cookie
                secure=False,   # Set to True in production if using HTTPS
                samesite='Strict', # CSRF protection
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Strict',
            )

            return response
        else:
            return Response({"error": "Authentication failed."}, status=status.HTTP_401_UNAUTHORIZED)




class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        # Your login logic here
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"success": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,  # Prevents JavaScript access
                secure=True,    # Set to True if using HTTPS
                samesite='Lax'  # Controls cross-site request handling
            )
            # Set refresh token in cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Strict"
            )

            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class InterpolationChartView(APIView):

    def post(self, request, *args, **kwargs):
        print("start")
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            # Validate token
            token = AccessToken(access_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token.')

        user = request.user  # Get the function and range from the request

        function_str = request.data.get('function')
        x_min = int(request.data.get('x_min'))
        x_max = int(request.data.get('x_max'))


        # Validate inputs
        if not function_str or not x_min or not x_max:
            return Response({"error": "Please provide function, x_min, and x_max."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the Celery task to generate the chart asynchronously
        result = generate_chart.apply_async(args=(function_str, x_min, x_max, user.id), queue='generate_chart_queue')

        # Wait for the task to finish and get the result (base64-encoded chart)

        print("we are here")
        task_id = result.task_id
        print(result)
        # Return the chart as a base64-encoded PNG image
        return Response({'task_id': task_id}, status=status.HTTP_200_OK)


# View to check the status of a task
class CheckTaskStatusView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check task status using the task_id
        print(task_id)
        result = AsyncResult(task_id)

        print(result.ready())

        if result.state == 'REVOKED':
            print("revoked")
            return Response({"status": "canceled"}, status=status.HTTP_200_OK)

        elif result.state == 'PENDING':
            print(result.result)
            print('pending')
            return Response({"status": "pending"}, status=status.HTTP_200_OK)

        elif result.state == 'SUCCESS':
            print(result.result)
            print("success")
            # Task is complete, return the result (chart)
            return Response({"chart": result.result["chart"]}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Task failed or was revoked"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cancel_task(request):
    task_id = request.data.get("task_id")
    print(task_id)
    if not task_id:
        return Response({"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    result = AsyncResult(task_id)
    result.revoke(terminate=True)  # Terminate the task
    print(result.status)
    print(result.result)

    return Response({"message": "Task canceled successfully"}, status=status.HTTP_200_OK)

class UserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = History.objects.filter(user=request.user).order_by('-created_at')
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data)


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # This endpoint will return the user information if authenticated
        user = request.user
        return Response({"username": user.username}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"error": "Refresh token not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            response = Response({"message": "Token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=str(new_access_token),
                httponly=True,
                secure=True,
                samesite="Lax"
            )
            return response
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')  # Delete the access token cookie
        return response
