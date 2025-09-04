from django.core.management.base import BaseCommand
from ip_tracking.models import RequestLog


class Command(BaseCommand):
    help = "Display recent IP request logs with country and city"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="Number of recent logs to display (default: 20)",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        logs = RequestLog.objects.order_by("-timestamp")[:limit]

        if not logs:
            self.stdout.write(self.style.WARNING("No request logs found."))
            return

        for log in logs:
            self.stdout.write(
                f"[{log.timestamp:%Y-%m-%d %H:%M:%S}] "
                f"{log.ip_address:<15} "
                f"{log.path:<20} "
                f"{(log.country or 'N/A')}, {(log.city or 'N/A')}"
            )
