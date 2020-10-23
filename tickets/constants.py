from django.db import models
from django.utils.translation import gettext_lazy as _


class TicketStatusType(models.TextChoices):
    PAID = "paid", _("Paid")
    CANCELED = "canceled", _("Canceled")
    BOOKED = "booked", _("Booked")
    UNPAID = "unpaid", _("Unpaid")


class TicketType(models.TextChoices):
    REGULAR = "regular", _("Regular")
    PREMIUM = "premium", _("Premium")
    VIP = "vip", _("Vip")