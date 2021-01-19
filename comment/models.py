from django.db import models
from django.contrib.auth import get_user_model

class comment(models.Model):
    user                        = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment                     = models.CharField(max_length=255)
    on                          = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Rahul comment on Ganesh that "You are doing a great job"
    # then Rahul - user
    # on - Ganesh
    date_of_comment     = models.DateTimeField(auto_now_add=True)

class comment_reply(models.Model):
    comment_id      = models.ForeignKey(comment, on_delete=models.CASCADE)      

