from django.contrib.auth import get_user_model
from product.models import product_details
from django.db import models


class cart(models.Model):
    user    = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    product = models.ForeignKey(product_details, on_delete= models.CASCADE)
