from django.db import models
from django.utils.translation import gettext_lazy as _


class EventStatusType(models.TextChoices):
    ACTIVE = "active", _("Active")
    POSTPONED = "postponed", _("Postponed")
    CANCELED = "canceled", _("Canceled")
    COMPLETED = "completed", _("Completed")
