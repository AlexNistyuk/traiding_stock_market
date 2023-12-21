# Generated by Django 5.0 on 2023-12-19 11:52

from decimal import Decimal

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brokers", "0003_rename_owner_limitorder_portfolio_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="investmentportfolio",
            constraint=models.CheckConstraint(
                check=models.Q(("spend_amount__gte", Decimal("0"))),
                name="investment_portfolio_spend_amount_non_negative",
            ),
        ),
    ]
