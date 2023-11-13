# Generated by Django 4.1 on 2023-11-13 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("testing", "0001_initial"),
        ("dataset", "0005_alter_dataset_author"),
        ("ranking", "0002_credit_credit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="credit",
            name="LLM",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testing.llms"
            ),
        ),
        migrations.AlterField(
            model_name="credit",
            name="credit",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="credit",
            name="dataset",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="dataset.dataset"
            ),
        ),
    ]
