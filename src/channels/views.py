from rest_framework import generics, viewsets, parsers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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
        return models.Channel.objects.filter(user=self.request.user). \
            prefetch_related('subscribers')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailChannelView(generics.RetrieveAPIView):
    serializer_class = serializers.DetailChannelSerializer
    queryset = models.Channel.objects.all()


class SubscriberView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            channel = models.Channel.objects.get(pk=pk)
            sub = models.Subscriber.objects.filter(channel=pk)
            serializer = serializers.SubscriberSerializer(sub, many=True)
            return Response(serializer.data)
        except models.Channel.DoesNotExist:
            return Response('Channel does not exists')
