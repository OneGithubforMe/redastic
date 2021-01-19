from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ajax/load_index_page_content', views.load_index_page_content, name="load_index_page_content"),
    #path('feedback', views.feedback),    
]
