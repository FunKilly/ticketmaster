# Generated by Django 3.0.4 on 2020-10-24 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20201024_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userticket',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tickets', to='tickets.Ticket'),
        ),
    ]