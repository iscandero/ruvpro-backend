# Generated by Django 4.0.4 on 2022-06-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0026_alter_user_social_networks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsocial',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
    ]