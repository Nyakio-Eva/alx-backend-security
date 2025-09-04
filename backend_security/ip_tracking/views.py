from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit


@csrf_exempt
@ratelimit(key="ip", rate="10/m", method="POST", block=True)   # Authenticated
@ratelimit(key="ip", rate="5/m", method="POST", block=True)    # Anonymous
def login_view(request):
    """
    Simple login view with IP-based rate limiting.
    - Authenticated users: 10 requests/minute
    - Anonymous users: 5 requests/minute
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"message": "Send a POST request with username & password"})
