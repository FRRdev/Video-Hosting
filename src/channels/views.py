from rest_framework import generics, viewsets, parsers, views

from . import serializers, models
from ..base.classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor


class ChannelView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateChannelSerializer
    serializer_class_by_action = {
        'list': serializers.ListChannelSerializer
    }

    def get_queryset(self):
        return models.Channel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailChannelView(generics.RetrieveAPIView):
    serializer_class = serializers.ListChannelSerializer
    queryset = models.Channel.objects.all()
