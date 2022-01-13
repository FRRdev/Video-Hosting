from rest_framework import generics, viewsets, parsers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers, models
from ..base.classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor


class ChannelView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD of Channel
    """
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
    """View for retrieve channel
    """
    serializer_class = serializers.DetailChannelSerializer
    queryset = models.Channel.objects.all()


class SubscriberView(APIView):
    """View to subscribe and unsubscribe to the channel
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            channel = models.Channel.objects.get(pk=pk)
            sub = models.Subscriber.objects.filter(channel=pk)
            serializer = serializers.SubscriberSerializer(sub, many=True)
            return Response(serializer.data)
        except models.Channel.DoesNotExist:
            return Response('Channel does not exists')

    def post(self, request, pk):
        try:
            channel = models.Channel.objects.get(pk=pk)
            sub = models.Subscriber.objects.filter(channel=pk, subscriber=request.user.pk)
            if sub.exists():
                sub.delete()
                return Response('you are no a subscriber anymore')
            else:
                sub = models.Subscriber.objects.create(channel=channel, subscriber=request.user)
                sub.save()
                return Response('you are a subscriber')
        except models.Channel.DoesNotExist:
            return Response('Channel does not exists')
