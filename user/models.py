from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from cart.models import Order, OrderItem
from store.models import Product

#Create the address model here 

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')
    apartment = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin = models.PositiveIntegerField()
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_absolute_update_url(self):
        return reverse("update-address", kwargs={"pk": self.pk})
    

    class Meta:
        verbose_name_plural = 'Addresses'

class Customer(models.Model):
    user= models.OneToOneField(User,related_name='customer',on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150,default='user1')
    address= models.OneToOneField(Address,related_name='customer',on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username


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