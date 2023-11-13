# Generated by Django 4.1 on 2023-11-13 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0011_resetpassword"),
        ("dataset", "0002_dataset_data_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="user.user",
            ),
            preserve_default=False,
        ),
    ]
