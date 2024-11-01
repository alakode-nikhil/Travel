# Generated by Django 5.1.1 on 2024-10-28 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="destination",
            name="weather",
            field=models.IntegerField(
                choices=[
                    (1, "Sunny"),
                    (2, "Rainy"),
                    (3, "Cloudy"),
                    (4, "Foggy"),
                    (5, "Snowy"),
                    (6, "Windy"),
                ]
            ),
        ),
    ]
