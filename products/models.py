from django.db import models


# Create your models here.
# Product Model.
class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=100, blank=False)
