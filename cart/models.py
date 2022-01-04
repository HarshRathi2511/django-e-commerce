from django.db import models
from store.models import Product,Category
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

# whenever add to cart pressed product becomes an OrderItem
class OrderItem(models.Model):  # link between the product and the order
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} :- {self.item.title}"

    def get_price_of_product(self):
        return self.quantity*self.item.price    
 

# final cart
class Order(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    items= models.ManyToManyField(OrderItem)
    ordered_date= models.DateTimeField()

    def __str__(self):
        return f"Order by :-{self.user.email}"

    def get_num_of_cart_items(self):
        return self.items.all().count()    

    def get_total_price_of_cart(self):
        total_price_cart=0
        for item in self.items.all():
            total_price_cart=total_price_cart+item.get_price_of_product()
        return total_price_cart    





