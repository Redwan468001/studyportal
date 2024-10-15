from django import forms
from .models import Room, Message


class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


# Message create form
class CreateMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = {'body'}