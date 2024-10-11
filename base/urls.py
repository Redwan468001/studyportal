from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:id>', views.room, name="room"),
    path('topic/<int:id>', views.topic, name="topic"),
    path('createroom', views.createroom, name="createroom"),
    path('room/edit/<int:id>', views.editroom, name="edit-room"),
]
