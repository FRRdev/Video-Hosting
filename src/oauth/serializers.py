from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = models.AuthUser
        fields = ('avatar', 'country', 'city', 'bio', 'display_name')

class UserSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = models.AuthUser
        fields = ('id', 'email', 'display_name', 'social_links')


class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SocialLink
        fields = ('id', 'link')


class AuthorSerializer(serializers.ModelSerializer):
    """"""
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = ('id', 'email', 'avatar', 'country', 'city', 'bio', 'display_name', 'social_links')


class GoogleAuth(serializers.Serializer):
    """Сериализация данных от гугл
    """
    email = serializers.EmailField()
    token = serializers.CharField()
