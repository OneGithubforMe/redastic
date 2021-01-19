from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search), 
    path('ajax/all_filter_in_serach', views.all_filter_in_serach, name="all_filter_in_serach"),
]
