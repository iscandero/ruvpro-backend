# Generated by Django 4.0.4 on 2022-06-23 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_projectemployee_role_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectemployee',
            name='role_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.role', verbose_name='ID Роли пользователя'),
        ),
    ]