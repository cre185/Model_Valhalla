# Generated by Django 4.1 on 2023-11-30 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LLMs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('api_url', models.CharField(default='http://111.202.73.146:10510/v1/chat/completions', max_length=255)),
                ('model_name', models.CharField(default='mistral_7b', max_length=255)),
                ('api_RPM', models.IntegerField(null=True)),
                ('logo', models.ImageField(default='static/logo/default.jpg', upload_to='static/logo')),
                ('official_website', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('document_name', models.TextField(default='')),
                ('document_website', models.TextField(default='')),
                ('license', models.TextField(default='')),
                ('elo_credit', models.FloatField(default=1500)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('released_time', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BattleHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('result', models.JSONField()),
                ('user_id', models.IntegerField()),
                ('winner', models.IntegerField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('llm1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='llm1', to='testing.llms')),
                ('llm2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='llm2', to='testing.llms')),
            ],
        ),
    ]
