from rest_framework import serializers
from . import models
from ..base.services import delete_old_file
from ..oauth.serializers import AuthorSerializer


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text')


class VideoSerializerForChannel(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = models.Video
        fields = ['id', 'title', 'genre', 'create_at', 'plays_count', 'download', 'private']


class CreateAuthorVideoSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Video
        fields = (
            'id',
            'title',
            'license',
            'genre',
            'playlist',
            'link_of_author',
            'file',
            'create_at',
            'plays_count',
            'download',
            'private',
            'cover',
            'user',
            'channel',
            'user_of_likes',
            'likes_count'
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class AuthorVideoSerializer(CreateAuthorVideoSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    user = AuthorSerializer()


class CreatePlayListSerializer(BaseSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'videos')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    videos = AuthorVideoSerializer(many=True, read_only=True)


class CommentAuthorSerializer(serializers.ModelSerializer):
    """Сериализация комментариев
    """

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'video')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев
    """
    user = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'video', 'create_at')
