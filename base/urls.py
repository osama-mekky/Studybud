from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>',views.room,name='room'),
    path('create-room',views.createRoom,name='create-room'),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delate-room/<str:pk>',views.delateRoom,name='delate-room'),
    path('delate-message/<str:pk>',views.delate_message,name='delate-message'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('register',views.register_page,name='register'),
    path('profile/<str:pk>',views.userProfile,name='profile'),
    path('update-user/',views.updateUser,name='update-user'),
    path('topics/',views.topicsPage,name='topics'),
    path('activity/',views.activityPage,name='activity'),


]

