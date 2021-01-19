from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login', views.login),
    path('register', views.register, name='register'),
    path('logout', views.logout),
    path('profile', views.profile),
    path('profile/<int:user_id>', views.profile_for_other),
    path('edit_profile', views.edit_profile),

]
