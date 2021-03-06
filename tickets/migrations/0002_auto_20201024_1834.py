# Generated by Django 3.0.4 on 2020-10-24 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20201024_1833'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='number_of_seats',
        ),
        migrations.RemoveField(
            model_name='userticket',
            name='price',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.Event'),
        ),
    ]
