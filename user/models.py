from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from cart.models import Order, OrderItem
from store.models import Product


# Create the profile model here 
class Profile(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    balance = models.DecimalField(decimal_places=2,default=200,max_digits=5)

    def __str__(self) :
      return f'${self.balance}'

    def get_balance(self):
        return self.balance  

    def update_balance(self,amount):
        self.balance = self.balance- amount  
        print(self.balance)
              


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE,related_name='reviews')
    description= models.TextField(blank=True)
    

    def __str__(self):
        return f"Review by {self.user} "


class UserDetail(models.Model):	
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='user_detail')
	dob = models.DateField(null = True)
	mobile = models.CharField(max_length=10,null=True,)
	address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50, null=True)
  
        