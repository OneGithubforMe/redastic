from django.contrib import admin
from .models import * 

admin.site.register(user_feedback)
admin.site.register(feedback_without_email)
admin.site.register(feedback_with_email)


