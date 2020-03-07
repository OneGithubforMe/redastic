from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_product),
    path('add/draft/', views.add_product_draft),
    path('view/<int:product_id>', views.product_detail_view),
#    path('owner_view/<int:product_id>', views.owner_detail_view),
    path('edit/<int:product_id>', views.product_edit),
    path('delete/<int:product_id>', views.product_delete),
    path('change_publish/<int:product_id>', views.change_publish_draft)         # better to use AJAX for this.
]
