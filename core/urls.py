from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('create-room', views.create_room_view, name='create-room'),
    path('update-room/<str:pk>', views.update_room_view, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room_view, name='delete-room'),
    path('room/<str:pk>', views.room_page, name='room'),

    path('create-channel/<str:pk>', views.create_channel, name='create-channel'),
    path('delete-channel/<str:pk>', views.delete_channel, name='delete-channel'),
    path('update-channel/<str:pk>', views.update_channel, name='update-channel'),

    path('channel/<str:pk>', views.channel_page, name='channel'),
    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
    path('join/<str:pk>', views.join_room, name='join'),
    path('disjoin/<str:pk>', views.leave_room, name='disjoin'),
]