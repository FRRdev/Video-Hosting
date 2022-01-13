from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .. import serializers
from ..services import google, spotify


def google_login(request):
    """Google login page
    """
    return render(request, 'oauth/google_login.html')


def spotify_login(request):
    """Spotify login page
    """
    return render(request, 'oauth/spotify_login.html')


@api_view(["POST"])
def google_auth(request):
    """Confirmation of authorization over Google
    """
    google_data = serializers.GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = google.check_google_auth(google_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data Google')


@api_view(["GET"])
def spotify_auth(request):
    """Confirmation of authorization over Spotify
    """
    token = spotify.spotify_auth(request.query_params.get('code'))
    return Response(token)
