from django import forms
from .models import Room,Channel

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name', 'description'
        ]

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'description']