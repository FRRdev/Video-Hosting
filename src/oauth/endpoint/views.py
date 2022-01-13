from rest_framework import viewsets, parsers, permissions
from rest_framework.permissions import IsAuthenticated

from .. import serializers, models
from ...base.permissions import IsAuthor


class UserView(viewsets.ModelViewSet):
    """Viewing and editing user data
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """List of Authors
    """
    queryset = models.AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = serializers.AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """CRUD user's social links
    """
    serializer_class = serializers.SocialLinkSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
