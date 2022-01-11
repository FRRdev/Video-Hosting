# Generated by Django 4.0 on 2022-01-11 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
        ('video_library', '0006_playlist_channel_video_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='user_of_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes_of_videos', to='oauth.AuthUser'),
        ),
    ]
