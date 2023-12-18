# Generated by Django 5.0 on 2023-12-16 08:19

from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("brokers", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="investmentportfolio",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="portfolio",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="limitorder",
            name="investment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="brokers.investment"
            ),
        ),
        migrations.AddField(
            model_name="limitorder",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="brokers.investmentportfolio",
            ),
        ),
        migrations.AddField(
            model_name="marketorder",
            name="investment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="brokers.investment"
            ),
        ),
        migrations.AddField(
            model_name="marketorder",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="brokers.investmentportfolio",
            ),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="investment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="brokers.investment"
            ),
        ),
        migrations.AddField(
            model_name="trade",
            name="buyer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="buyer",
                to="brokers.investmentportfolio",
            ),
        ),
        migrations.AddField(
            model_name="trade",
            name="investment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="brokers.investment"
            ),
        ),
        migrations.AddField(
            model_name="trade",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="seller",
                to="brokers.investmentportfolio",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="investmentportfolio",
            unique_together={("owner", "investment")},
        ),
        migrations.AddConstraint(
            model_name="limitorder",
            constraint=models.CheckConstraint(
                check=models.Q(("price__gte", Decimal("0"))),
                name="limit_order_price_non_negative",
            ),
        ),
        migrations.AddConstraint(
            model_name="trade",
            constraint=models.CheckConstraint(
                check=models.Q(("price__gte", Decimal("0"))),
                name="trade_price_non_negative",
            ),
        ),
    ]
