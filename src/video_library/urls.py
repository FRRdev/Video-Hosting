from django.urls import path
from . import views

urlpatterns = [
    path('genre/', views.GenreView.as_view()),

    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>/', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('video/', views.TrackView.as_view({'get': 'list', 'post': 'create'})),
    path('video/<int:pk>/', views.TrackView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('stream-video/<int:pk>/', views.StreamingFileView.as_view()),
    path('download-video/<int:pk>/', views.DownloadTrackView.as_view()),

    path('stream-author-video/<int:pk>/', views.StreamingFileAuthorView.as_view()),

    path('video-list/', views.TrackListView.as_view()),
    path('author-video-list/<int:pk>/', views.AuthorTrackListView.as_view()),

    path('comments/', views.CommentAuthorView.as_view({'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', views.CommentAuthorView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('comments_by_video/<int:pk>/', views.CommentView.as_view({'get': 'list'})),

    path('playlist/', views.PlayListView.as_view({'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', views.PlayListView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('like/<int:pk>', views.LikeView.as_view()),
]
