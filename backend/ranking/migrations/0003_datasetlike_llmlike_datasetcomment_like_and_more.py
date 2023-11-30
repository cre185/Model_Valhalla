# Generated by Django 4.1 on 2023-11-16 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
        ("ranking", "0002_llmcomment_datasetcomment"),
    ]

    operations = [
        migrations.CreateModel(
            name="DatasetLike",
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
            ],
        ),
        migrations.CreateModel(
            name="LLMLike",
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
            ],
        ),
        migrations.AddField(
            model_name="datasetcomment",
            name="like",
            field=models.ManyToManyField(
                related_name="dataset_comment_like",
                through="ranking.DatasetLike",
                to="user.user",
            ),
        ),
        migrations.AddField(
            model_name="llmcomment",
            name="like",
            field=models.ManyToManyField(
                related_name="llm_comment_like",
                through="ranking.LLMLike",
                to="user.user",
            ),
        ),
        migrations.AddField(
            model_name="llmlike",
            name="comment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ranking.llmcomment"
            ),
        ),
        migrations.AddField(
            model_name="llmlike",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="user.user"
            ),
        ),
        migrations.AddField(
            model_name="datasetlike",
            name="comment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ranking.datasetcomment"
            ),
        ),
        migrations.AddField(
            model_name="datasetlike",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="user.user"
            ),
        ),
    ]
