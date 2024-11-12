# urls.py
from django.urls import path
from .views import (RegisterUserView, LoginUserView, InterpolationChartView, UserHistoryView, UserMeView,
                    RefreshTokenView, LogoutUserView, cancel_task, CheckTaskStatusView)




urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('generate-chart/', InterpolationChartView.as_view(), name='generate-chart'),
    path('history/', UserHistoryView.as_view(), name='user-history'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('cancel-task/', cancel_task, name='cancel_task'),
    path('check-task-status/', CheckTaskStatusView.as_view(), name='check_task_status'),  # URL to check task status
]
