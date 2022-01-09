from django.db import models
from store.models import Product,Category
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from vendor.models import Vendor

# whenever add to cart pressed product becomes an OrderItem
class OrderItem(models.Model):  # link between the product and the order
    item = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_item')
    #get the order item by product.order_item 
    quantity = models.PositiveIntegerField(default=1)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.quantity} :- {self.item.title}"

    def get_price_of_product(self):
        return self.quantity*self.item.price 

    def get_product_slug(self):
        return self.item.slug 

    def get_order_item_vendor(self):
        return self.item.created_by         

    def get_review_url(self):
        return reversed('write-review',args=[self.item.slug])   
        
    def get_product(self):
        return self.item    
 

# final cart
class Order(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    items= models.ManyToManyField(OrderItem)
    ordered_date= models.DateTimeField()
    # vendors = models.ManyToManyField(Vendor, related_name='orders')

    def __str__(self):
        return f"Order by :-{self.user.email}"
        
    def return_order_items(self):
        return self.items.all()

    def get_num_of_cart_items(self):
        return self.items.all().count()    

    def get_total_price_of_cart(self):
        total_price_cart=0
        for item in self.items.all():
            total_price_cart=total_price_cart+item.get_price_of_product()
        return total_price_cart    





