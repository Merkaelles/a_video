# Generated by Django 3.2 on 2024-03-31 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_user_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_icon',
            field=models.FileField(blank=True, default='33.jpg', max_length=255, null=True, upload_to='', verbose_name='头像'),
        ),
    ]
