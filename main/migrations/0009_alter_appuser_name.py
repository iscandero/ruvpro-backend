# Generated by Django 4.0.4 on 2022-07-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0008_alter_appuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Имя пользователя'),
        ),
    ]
