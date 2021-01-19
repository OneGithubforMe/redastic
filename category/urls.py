from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:category_id>', views.go_to_category),
    path('ajax/all_filter_in_category', views.all_filter_in_category, name="all_filter_in_category"),
    
]
