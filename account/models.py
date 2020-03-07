from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager 
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise  ValueError("user must have an email address")
        if not password:
            raise ValueError("user must have a password")
        if not full_name:
            raise ValueError("User must have a name")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )
        user_obj.set_password(password)     # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff = True
        )
        return user
    
    
    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user
    



class User(AbstractBaseUser):
    email           = models.EmailField(verbose_name='email', max_length=255, unique=True)
    full_name       = models.CharField(verbose_name='full Name', max_length=255, blank=False, null=False)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    active          = models.BooleanField(default=True)
    admin           = models.BooleanField(default=False)    # superuser
    staff           = models.BooleanField(default=False)    # staff non superuser


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin    

    @property
    def is_actice(self):
        return self.active


class profile_information(models.Model):                    
    user                        = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_picture             = models.ImageField(upload_to="pics/account/profile_picture", verbose_name='Profile Picture', default='default/user_default_img.jpg')     #
    phone_number                = models.CharField(verbose_name='phone number', max_length=10)   # change this
    is_email_verified           = models.BooleanField(default=False)          # via OTP
    is_phone_number_verified    = models.BooleanField(default=False)          # via OTP
    
    
    def __str__(self):  
        return self.phone_number
    
    def get_user_img(self):
        return self.profile_picture
