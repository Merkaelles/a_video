# Generated by Django 3.2 on 2024-03-28 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_rename_owner_video_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='display_time',
            new_name='play_time',
        ),
        migrations.RemoveField(
            model_name='video',
            name='display_times',
        ),
        migrations.AddField(
            model_name='video',
            name='play_times',
            field=models.IntegerField(blank=True, null=True, verbose_name='播放次数'),
        ),
    ]
