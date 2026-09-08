from django.urls import path
from . import views

urlpatterns = [
    path('conversation/<str:pk>', views.conversation_page, name='conversation'),
    path('conversations/<str:pk>', views.all_messages, name='conversations'),
    path('create-conversation/<str:pk>', views.create_conversation, name='create-conversation'),
    path('delete-conversation/<str:pk>', views.delete_conversation, name='delete-conversation'),
    path('delete-conversation-message/<str:pk>', views.delete_conversation_message, name='delete-conversation-message')
]