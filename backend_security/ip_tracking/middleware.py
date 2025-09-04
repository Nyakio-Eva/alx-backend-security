import requests
from .models import RequestLog, BlockedIP
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.core.cache import cache


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP (handles proxies if set)
        ip_address = self.get_client_ip(request)
        path = request.path
        
        # Check blacklist
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

         # Cache key
        cache_key = f"geo_{ip_address}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            geo_data = self.get_geo_data(ip_address)
            cache.set(cache_key, geo_data, 60 * 60 * 24)  # 24h cache

        # Save log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path,
            country=geo_data.get("country"),
            city=geo_data.get("city"),
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
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def get_geo_data(self, ip):
        try:
            r = requests.get(f"https://ipapi.co/{ip}/json/").json()
            return {
                "country": r.get("country_name"),
                "city": r.get("city"),
            }
        except Exception:
            return {"country": None, "city": None}
