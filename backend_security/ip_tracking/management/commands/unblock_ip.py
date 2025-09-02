from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Unblock an IP address by removing it from the BlockedIP model"

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="IP address to unblock")

    def handle(self, *args, **options):
        ip = options["ip_address"]

        try:
            blocked_ip = BlockedIP.objects.get(ip_address=ip)
            blocked_ip.delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully unblocked IP: {ip}"))
        except BlockedIP.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"IP {ip} was not in the blacklist."))
