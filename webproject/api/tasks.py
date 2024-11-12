from django.contrib.auth.models import User

from .models import History
from celery import shared_task
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sympy import symbols, sympify
from scipy.interpolate import interp1d
import math
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from celery.exceptions import Ignore
import time



def manual_function_evaluation(func, x):
    """Manually evaluate the function by approximating the result."""
    # Here we are just doing a simple approximation of a function using a loop.
    result = 0
    for i in range(1, 1000000):
        result += (x ** i) / math.factorial(i)  # Example of a slow approximation
    return result


def manual_interpolation(x_vals, y_vals, x):
    """Manually interpolate using linear interpolation."""
    # Assuming x_vals and y_vals are sorted
    for i in range(1, len(x_vals)):
        if x_vals[i] >= x:
            x0, y0 = x_vals[i-1], y_vals[i-1]
            x1, y1 = x_vals[i], y_vals[i]
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return y_vals[-1]  # If x is out of bounds, return the last y value


x = symbols('x')


@shared_task(bind=True)
@permission_classes([IsAuthenticated])
def generate_chart(self, function_str, x_min, x_max, user_id, num_points=300000):
    try:
        print(f"Task {self.request.id} started")  # Print when the task starts

        # Fetch the user object
        user = User.objects.get(id=user_id)
        print(f"User found: {user.username}")  # Print user info to confirm retrieval

        # Parse the function string to a sympy expression
        func = sympify(function_str)
        print(f"Function parsed: {function_str}")  # Print the parsed function

        # Generate x and y values
        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals = np.array([float(func.subs(x, val)) for val in x_vals])
        print(f"Generated {len(x_vals)} x values and {len(y_vals)} y values")  # Check the number of points

        # Perform interpolation
        interpolation = interp1d(x_vals, y_vals, kind='linear', fill_value="extrapolate")
        x_fine = np.linspace(x_min, x_max, num_points * 10)
        y_fine = interpolation(x_fine)
        print(f"Interpolation complete, generated {len(x_fine)} fine points")  # Confirm interpolation

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, 'bo', label='Data points')
        plt.plot(x_fine, y_fine, 'r-', label='Interpolated curve')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Function Plot with Interpolation')
        plt.legend()

        # Save the plot to a BytesIO buffer and encode as base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print(f"Chart generated successfully, base64 length: {len(chart_base64)}")  # Check the base64 length

        # Save the chart to history
        task = History.objects.create(
            user=user,
            function_str=function_str,
            x_min=x_min,
            x_max=x_max,
            chart=chart_base64
        )
        print(f"History entry created with task ID: {task.id}")  # Confirm history entry

        return {'chart': chart_base64}

    except Exception as e:
        print(f"Error generating chart: {e}")  # Print any errors that occur
        return None  # Return None on error for now

from celery import shared_task

@shared_task(bind=True)
def test_task(self):
    time.sleep(3)
    print("Test task started")
    return "Test task completed"