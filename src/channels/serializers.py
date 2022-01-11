from rest_framework import serializers

from . import models
from src.oauth.serializers import AuthorSerializer, UserSerializerShort


class SubscriberSerializer(serializers.ModelSerializer):
    subscriber = UserSerializerShort(read_only=True)

    class Meta:
        model = models.Subscriber
        fields = ['subscriber',]


class CreateChannelSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Channel
        fields = (
            'user',
            'name',
            'description',
        )


class ListChannelSerializer(serializers.ModelSerializer):
    user = UserSerializerShort(read_only=True)
    subscribers = SubscriberSerializer(many=True)

    class Meta:
        model = models.Channel
        fields = (
            'user',
            'name',
            'description',
            'created_at',
            'subscribers',
        )
