# Generated by Django 4.0.4 on 2022-06-27 10:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0027_alter_newsocial_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social_networks',
        ),
        migrations.DeleteModel(
            name='NewSocial',
        ),
    ]