from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('feedback', views.feedback),
    # path('<id:category>', views.category),
    # path('/sort', views.category),
]
