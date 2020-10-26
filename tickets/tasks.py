from celery.decorators import task
from django.core.management import call_command


@task(name="update_statuses")
def update_statuses():
    call_command("update_statuses_command",)
