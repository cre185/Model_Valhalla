# Generated by Django 4.2.5 on 2023-11-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/avatar/default.jpg', upload_to='static/avatar'),
        ),
    ]