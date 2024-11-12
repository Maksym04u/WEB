# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import History


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_superuser=validated_data.get('is_superuser', False)
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['function_str', 'x_min', 'x_max', 'chart', 'created_at']