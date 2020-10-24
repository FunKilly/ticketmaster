from celery.decorators import task
from events.models import Event

@task(name="add_tickets")
def add_tickets(event_pk, data):
    event = Event.objects.filter(pk=event_pk).first()
    event.create_tickets(data)
