from django.db import models

from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length =250,db_index=True)
    slug = models.SlugField(max_length=255,unique=True) #the url with which a category is accessed

    class Meta:
        verbose_name_plural ='categories'

    def __str__(self):
        return self.name 

# The related_name attribute specifies the name of the reverse relation from the Category
#  model back to your Product,otherwise default product_set()
class Product(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=6,default=0)
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    created_by = models.ForeignKey(Vendor,related_name='product_creator',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'images/')
    slug = models.SlugField(max_length=250)
    in_stock= models.BooleanField(default=True)
    created_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date_time']

    def __str__(self):
        return self.title  