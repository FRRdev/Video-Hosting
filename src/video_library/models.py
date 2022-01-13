from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import (
    validate_size_image,
    get_path_upload_cover_album,
    get_path_upload_video,
    get_path_upload_cover_playlist,
    get_path_upload_cover_video
)
from src.oauth.models import AuthUser
from src.channels.models import Channel


class License(models.Model):
    """ Model user's video license
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1000)


class Genre(models.Model):
    """ Model of video genre
    """
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Model of video
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos_by_channel', default=1)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    license = models.ForeignKey(License, on_delete=models.PROTECT, related_name='license_videos')
    genre = models.ManyToManyField(Genre, related_name='video_genres')
    playlist = models.ForeignKey('PlayList', on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(
        upload_to=get_path_upload_video,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mp3', 'wav'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(AuthUser, related_name='likes_of_videos', null=True, blank=True)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_video,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    """ Model of video's comment
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)


class PlayList(models.Model):
    """ Model of user's playlists
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='playlists_by_channel', default=1)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video, related_name='video_play_lists')
    description = models.TextField(max_length=1000, null=True, blank=True)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_playlist,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )
