from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
# Create your models here.
class Vendor(models.Model):
      shop_name = models.CharField(max_length=250)
      owner= models.OneToOneField(User,related_name = 'vendor',on_delete=models.CASCADE)

      def __str__(self):
        return self.shop_name   #this is what comes in the admin area 

     