# Generated by Django 3.2 on 2024-03-31 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20240331_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationlog',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='update_time',
        ),
    ]
