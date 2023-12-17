# Generated by Django 4.1 on 2023-12-17 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
        ('user', '0001_initial'),
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respond_to', models.IntegerField(null=True)),
                ('comment', models.TextField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='LLMComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respond_to', models.IntegerField(null=True)),
                ('comment', models.TextField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectiveCredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_list', models.JSONField(default=list)),
                ('LLM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.llms')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='LLMLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislike', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.llmcomment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='llmcomment',
            name='like',
            field=models.ManyToManyField(related_name='llm_comment_like', through='ranking.LLMLike', to='user.user'),
        ),
        migrations.AddField(
            model_name='llmcomment',
            name='llm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.llms'),
        ),
        migrations.AddField(
            model_name='llmcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.CreateModel(
            name='DatasetLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislike', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.datasetcomment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='datasetcomment',
            name='like',
            field=models.ManyToManyField(related_name='dataset_comment_like', through='ranking.DatasetLike', to='user.user'),
        ),
        migrations.AddField(
            model_name='datasetcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.FloatField(null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('LLM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.llms')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset')),
            ],
        ),
    ]
