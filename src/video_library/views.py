import os

from django.http import FileResponse, Http404, HttpResponse
from rest_framework import generics, viewsets, parsers, views
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializer, models
from ..base.classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """List of video's genres
    """
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """ CRUD author's licenses
    """
    serializer_class = serializer.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD Videos
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializer.CreateAuthorVideoSerializer
    serializer_class_by_action = {
        'list': serializer.AuthorVideoSerializer
    }

    def get_queryset(self):
        return models.Video.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD user's playlists
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializer.CreatePlayListSerializer
    serializer_class_by_action = {
        'list': serializer.PlayListSerializer
    }

    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class VideoListView(generics.ListAPIView):
    """ List of videos
    """
    queryset = models.Video.objects.filter(private=False)
    serializer_class = serializer.AuthorVideoSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', ]
    filterset_fields = ['user__display_name', 'playlist__title', 'genre__name']


class AuthorVideoListView(generics.ListAPIView):
    """ List of author's videos
    """
    serializer_class = serializer.AuthorVideoSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'playlist__title', 'genre__name']

    def get_queryset(self):
        return models.Video.objects.filter(
            user__id=self.kwargs.get('pk'), playlist__private=False, private=False
        )


class CommentAuthorView(viewsets.ModelViewSet):
    """ CRUD author's comments
    """
    serializer_class = serializer.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """ Video's comments
    """
    serializer_class = serializer.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(video_id=self.kwargs.get('pk'))


class StreamingFileView(views.APIView):
    """ Streaming of video
    """

    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Video, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            # response = HttpResponse('', content_type="video/mp4", status=206)
            # response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            # return response
            return FileResponse(open(self.track.file.path, 'rb'), filename=self.track.file.name)
        else:
            return Http404


class DownloadVideoView(views.APIView):
    """ Download video
    """

    def set_download(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Video, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_download()
            # response = HttpResponse('', content_type="audio/mpeg", status=206)
            # response["Content-Disposition"] = f"attachment; filename={self.track.file.name}"
            # response['X-Accel-Redirect'] = f"/media/{self.track.file.name}"
            return FileResponse(open(self.track.file.path, 'rb'), filename=self.track.file.name, as_attachment=True)
        else:
            return Http404


class StreamingFileAuthorView(views.APIView):
    """ Streaming of author's video
    """
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.track = get_object_or_404(models.Video, id=pk, user=request.user)
        if os.path.exists(self.track.file.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404


class LikeView(views.APIView):
    """ Adding/removing like for video
    """
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        try:
            current_video = models.Video.objects.get(pk=pk)
            like_exists = models.Video.objects.filter(
                pk=pk, user_of_likes__pk=request.user.pk
            ).exists()
            if like_exists:
                current_video.user_of_likes.remove(request.user)
                current_video.likes_count -= 1
                current_video.save()
            else:
                current_video.user_of_likes.add(request.user)
                current_video.likes_count += 1
                current_video.save()
        except models.Video.DoesNotExist:
            response = HttpResponse('does not have video with this pk', status=206)
            return response
        response = HttpResponse('likes was changed successfully', status=206)
        return response
