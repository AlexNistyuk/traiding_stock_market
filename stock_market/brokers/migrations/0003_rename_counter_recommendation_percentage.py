# Generated by Django 5.0 on 2023-12-29 06:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("brokers", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recommendation",
            old_name="counter",
            new_name="percentage",
        ),
    ]
