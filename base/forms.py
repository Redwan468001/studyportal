from django import forms
from .models import Room, Message
from django.contrib.auth.models import User


# # User registration from
# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'email']

# Room create form
class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


# Message create form
class CreateMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = {'body'}