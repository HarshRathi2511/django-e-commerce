
from django.db import models
from django.urls import reverse
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length =250,db_index=True)
    slug = models.SlugField(max_length=255,unique=True) #the url with which a category is accessed

    class Meta:
        verbose_name_plural ='categories'

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('store:category_products', args=[self.slug])
        

# The related_name attribute specifies the name of the reverse relation from the Category
#  model back to your Product,otherwise default product_set()
class Product(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=6,default=0)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    created_by = models.ForeignKey(Vendor,related_name='products',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'images/')
    slug = models.SlugField(max_length=250)
    in_stock= models.BooleanField(default=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    stock= models.PositiveIntegerField(default=1)
  

    class Meta:
        ordering=['-created_date_time']

    def __str__(self):
        return self.title  

    def get_absolute_url(self):
        return reverse('store:product_detail',args=[self.slug])

    def get_add_to_cart_url(self):
        return reverse('cart:add-to-cart',args=[self.slug])

    def get_add_to_wishlist_url(self):
        return reverse('cart:add-to-wishlist',args=[self.slug])    

    def get_remove_from_cart_url(self):
        return reverse('cart:remove-from-cart',args=[self.slug])   

    def remove_single_item_from_cart_url(self): 
        return reverse('cart:remove-single-item-from-cart',args=[self.slug])  
        
    def get_delete_product_url(self):
        return reverse('vendor:delete-product',args=[self.slug])    

    def decrease_stock(self,quantity):
        self.stock= self.stock-quantity
        self.save()
        