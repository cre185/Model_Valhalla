# Generated by Django 4.1 on 2023-12-06 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dataset", "0001_initial"),
        ("testing", "0001_initial"),
        ("ranking", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubjectiveCredit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("credit_list", models.JSONField(default=list)),
                (
                    "LLM",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="testing.llms"
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dataset.dataset",
                    ),
                ),
            ],
        ),
    ]
