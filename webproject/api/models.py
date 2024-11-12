from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    function_str = models.CharField(max_length=255)
    x_min = models.FloatField()
    x_max = models.FloatField()
    chart = models.TextField()  # Store base64 chart
    created_at = models.DateTimeField(auto_now_add=True)
