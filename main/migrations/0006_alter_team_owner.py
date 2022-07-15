# Generated by Django 4.0.4 on 2022-07-04 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_team_participants_alter_team_owner_delete_usersteam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='owner',
                                       to='main.appuser', verbose_name='ID Создателя'),
        ),
    ]