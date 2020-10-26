from django.db import models
from django.utils.translation import gettext_lazy as _


class TicketStatusType(models.TextChoices):
    PAID = "paid", _("Paid")
    BOOKED = "booked", _("Booked")
    SPARE = "spare", _("Spare")


class TicketType(models.TextChoices):
    REGULAR = "regular", _("Regular")
    PREMIUM = "premium", _("Premium")
    VIP = "vip", _("Vip")


class OrderStatusType(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    UNPAID = "unpaid", _("Unpaid")
    PAID = "paid", _("Paid")
