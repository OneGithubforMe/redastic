from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import profile_information


User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The form to change user instenses
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # the fields to be used in displaying the user model 
    # these override the definitation on the base Usermodel 
    # that refresnce specific fields on auth.user
    list_display = ('email','full_name', 'admin', 'staff',)
    list_filter = ('admin', 'staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields' : ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')})
    )

    # add_fieldsets is not a standard Model admin attribute. UserAdmin 
    # overrides get_fieldset to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide', ), 
            'fields' : ('email', 'password')  
        }), 
    )

    search_fields = ('full_name', 'email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(profile_information)



'''
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm      # update view
    add_form = UserAdminCreationForm # create view
    # class Meta:
    #    model = User

admin.site.register(User, UserAdmin)




class AccountAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login','admin', 'staff')  # Contain only fields in your `custom-user-model`
    search_fields = ('email',)  # Contain only fields in your `custom-user-model` intended for searching
    readonly_fields = ('date_joined', 'last_login',)
    ordering = ()   # Contain only fields in your `custom-user-model` intended to ordering
    filter_horizontal = ()  # Leave it empty. You have neither `groups` or `user_permissions`
    list_filter = ()    # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    fieldsets = ()


User = get_user_model()
admin.site.register(User, AccountAdmin)

'''