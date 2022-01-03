from django.db import models
from store.models import Product,Category
from django.contrib.auth.models import User


# whenever add to cart pressed product becomes an OrderItem
class OrderItem(models.Model):  # link between the product and the order
    item = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.title




# final cart
class Order(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    items= models.ManyToManyField(OrderItem)
    ordered_date= models.DateTimeField()

    def __str__(self):
        return self.user


