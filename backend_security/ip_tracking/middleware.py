from .models import RequestLog, BlockedIP
from django.utils.timezone import now
from django.http import HttpResponseForbidden

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP (handles proxies if set)
        ip_address = self.get_client_ip(request)
        path = request.path

        # Save log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path
        )
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Log the request if not blocked
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP from request headers or remote addr."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
