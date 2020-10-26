from django.core.management.base import BaseCommand

from tickets.constants import OrderStatusType, TicketStatusType
from tickets.models import Order


class Command(BaseCommand):
    help = "Updating statuses for tickets and orders"

    def handle(self, *args, **options):
        self.stdout.write("Updating statuses has been launched.")
        active_orders = Order.objects.filter(status="waiting")

        for order in active_orders:
            if order.is_active is False:
                order.status = OrderStatusType.UNPAID
                order.ticket_set.update(status=TicketStatusType.SPARE)
                order.ticket_set.clear()
                order.save()
