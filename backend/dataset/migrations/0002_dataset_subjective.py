# Generated by Django 4.1 on 2023-11-16 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataset", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="subjective",
            field=models.BooleanField(default=False),
        ),
    ]
