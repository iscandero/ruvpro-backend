# Generated by Django 4.0.4 on 2022-07-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_project_assists_work_time_project_interns_work_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='refresh_token_data',
            field=models.TextField(blank=True, null=True, verbose_name='token'),
        ),
    ]