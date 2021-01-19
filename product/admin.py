from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import * 

User = get_user_model()


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'user')

admin.site.register(product_category)
admin.site.register(product_rent_type)
admin.site.register(product_details, ProductDetailsAdmin)
admin.site.register(product_img)
admin.site.register(product_profile_img)
#admin.site.register(product_owner_condition)
admin.site.register(product_available_location)
admin.site.register(product_question)
admin.site.register(answer)

