from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:id>', views.room, name="room"),
    path("sign-up/", views.registrationpage, name="sign-up"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutview, name="logout"),
    path('topic/<int:id>', views.topic, name="topic"),
    path('createroom', views.createroom, name="createroom"),
    path('room/edit/<int:id>', views.editroom, name="edit-room"),
    path('room/delete/<int:id>', views.deleteroom, name="delete_room"),
    path('del-message/<int:id>', views.deletemessage, name="del_message"),
]
