# Generated by Django 4.1 on 2023-11-30 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
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
                ("name", models.CharField(max_length=127)),
                (
                    "data_file",
                    models.FileField(
                        default="static/data/ceval_select.csv", upload_to="static/data"
                    ),
                ),
                ("content_size", models.IntegerField(default=200)),
                ("add_time", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField(default="")),
                ("subjective", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.user",
                    ),
                ),
            ],
        ),
    ]
