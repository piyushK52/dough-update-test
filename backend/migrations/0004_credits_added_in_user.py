# Generated by Django 4.2.1 on 2023-08-02 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_custom_trained_model_check_added"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="total_credits",
            field=models.FloatField(default=0),
        ),
    ]