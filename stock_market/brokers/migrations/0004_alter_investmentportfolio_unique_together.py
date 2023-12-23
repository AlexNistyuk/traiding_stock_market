# Generated by Django 5.0 on 2023-12-23 08:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("brokers", "0003_rename_owner_limitorder_portfolio_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="investmentportfolio",
            unique_together={("owner", "investment")},
        ),
    ]
