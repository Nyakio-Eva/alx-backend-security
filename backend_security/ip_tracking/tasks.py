from celery import shared_task
from django.utils import timezone
from django.db import models 
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_anomalies():
    """
    Flags suspicious IPs based on request volume and sensitive path access.
    Runs hourly.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # --- Rule 1: Too many requests (>100/hour) ---
    request_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(count=models.Count("id"))
    )

    for entry in request_counts:
        if entry["count"] > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=entry["ip_address"],
                reason=f"High traffic: {entry['count']} requests in the last hour",
            )

    # --- Rule 2: Sensitive path access ---
    sensitive_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS
    )
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}",
        )
