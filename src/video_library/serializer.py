from rest_framework import serializers
from . import models
from ..base.services import delete_old_file
from ..oauth.serializers import AuthorSerializer


class BaseSerializer(serializers.ModelSerializer):
    """ Base serializer for id
    """
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    """ Serializer for video's genre
    """
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class LicenseSerializer(BaseSerializer):
    """ Serializer for video's license
    """
    class Meta:
        model = models.License
        fields = ('id', 'text')


class VideoSerializerForChannel(serializers.ModelSerializer):
    """ Serializer for video to
    """
    genre = GenreSerializer(many=True)

    class Meta:
        model = models.Video
        fields = ['id', 'title', 'genre', 'create_at', 'plays_count', 'download', 'private']


class CreateAuthorVideoSerializer(BaseSerializer):
    """ Serializer for creating video
    """
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
    """ Serializer for author's video
    """
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    user = AuthorSerializer()


class CreatePlayListSerializer(BaseSerializer):
    """ Serializer for creating playlist
    """
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'videos')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    """ Serializer channel's playlist
    """
    videos = AuthorVideoSerializer(many=True, read_only=True)


class CommentAuthorSerializer(serializers.ModelSerializer):
    """ Serializer for comment
    """

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'video')


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer for comment(expended)
    """
    user = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'video', 'create_at')
