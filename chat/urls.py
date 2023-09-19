from django.urls import path, include

from .views import index, room

urlpatterns = [
    path('', index, name='chat-page'),
    path('<str:room_name>/', room, name='room-page'),
]
