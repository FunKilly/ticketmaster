import uuid

from django.db import models
from django.core.validators import MinValueValidator

from .constants import EventStatusType

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, blank=False, null=False)
    event_date = models.DateTimeField(blank=False, null=False)
    place = models.CharField(max_length=200, blank=False, null=False)
    total_seats = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=EventStatusType.choices, default=EventStatusType.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def places_available(self):
        # ilość miejsc - odwrócona relacja z biletem  *count*
        pass
    