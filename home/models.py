from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class user_feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    feedback = models.TextField()
 


class feedback_without_email(models.Model):
    feedback = models.TextField()



class feedback_with_email(models.Model):
    email = models.EmailField()
    feedback = models.TextField()
    