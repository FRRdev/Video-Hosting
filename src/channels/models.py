from django.db import models
from src.oauth.models import AuthUser


class Channel(models.Model):
    """Модель Канала ползователя
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Subscriber(models.Model):
    """Модель подписчиков на канал
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribed_channels')

    class Meta:
        unique_together = ["channel", "subscriber"]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.channel}'
