from django.contrib import admin
from django.urls import path
from MainApp import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('about', views.about),
    path('login', views.loginUser),
    path('logout', views.logoutUser),
    path('verification', views.userVerify),
    path('forgotPass/<int:page>', views.forgotPage, name='forgotPage'),
    path('register', views.registerUser),
    path('getdata', views.getdata),
    path('deleteNote', views.deleteNote),
    path('editNote/<int:note_id>', views.editNote),
    path('shareNote/<int:note_id>', views.shareNote),
    path('search', views.search),
]
