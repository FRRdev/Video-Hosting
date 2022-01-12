from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChannelView.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', views.ChannelView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('detail/<int:pk>/', views.DetailChannelView.as_view()),
    path('subscriber/<int:pk>/', views.SubscriberView.as_view()),
]
