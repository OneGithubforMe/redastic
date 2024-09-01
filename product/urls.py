from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_product),
    path('add/draft/', views.add_product_draft),
    path('view/<int:product_id>', views.product_detail_view),
#    path('owner_view/<int:product_id>', views.owner_detail_view),
    path('delete/<int:product_id>', views.product_delete),
    path('edit/<int:product_id>', views.product_edit),
    path('question/<int:product_id>', views.ask_question),
    path('question/delete/<int:question_id>', views.delete_question),
    path('answer/<int:question_id>', views.answer_of_question),
    path('answer/delete/<int:answer_id>', views.delete_answer),
    path('change_publish/<int:product_id>', views.change_publish_draft),                # better to use AJAX for this.
    path('edit/cpi/<int:img_id>', views.change_product_img),                            # cpi - change product image
    path('edit/rpi/<int:img_id>', views.remove_product_img),                            # rpi - remove product image
    path('edit/cppi/<int:img_id>', views.change_product_profile_img),                   # cppi - change product profile image 
    path('edit/<int:product_id>/api', views.add_product_img),                           # api - add product image
    
]
