# Generated by Django 3.0.4 on 2020-10-25 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20201024_1833'),
        ('users', '0004_remove_user_tickets'),
        ('tickets', '0006_auto_20201025_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('unpaid', 'Unpaid'), ('paid', 'Paid')], default='waiting', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Event')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='status',
        ),
        migrations.DeleteModel(
            name='PaymentHistory',
        ),
        migrations.DeleteModel(
            name='UserTicket',
        ),
        migrations.AddField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.Order'),
        ),
    ]