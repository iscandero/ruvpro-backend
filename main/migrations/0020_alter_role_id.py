# Generated by Django 4.0.4 on 2022-06-23 20:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0019_alter_role_is_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
    ]