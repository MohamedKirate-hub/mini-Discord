from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>', views.profile_view, name='profile'),
    path('edite/<str:pk>', views.update_profile_view, name='edite-profile')
]