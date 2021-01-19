from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('view', views.view_cart),
    path('ajax/add/<int:product_id>', views.add_in_cart, name="add_to_cart"),
    path('remove/<int:product_id>', views.remove_from_cart, name="remove_from_cart"),
]
