from rest_framework import serializers

from . import models
from src.oauth.serializers import AuthorSerializer


class CreateChannelSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Channel
        fields = (
            'user',
            'name',
            'description',
        )


class ChannelSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Channel
        fields = (
            'user',
            'name',
            'description',
            'created_at',
        )
