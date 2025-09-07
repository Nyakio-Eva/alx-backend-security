from django.apps import AppConfig
import os


class IpTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_security.ip_tracking'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":  # prevent double run
            from celery import current_app
            current_app.worker_main(["worker", "-A", "backend_security", "-l", "info"])