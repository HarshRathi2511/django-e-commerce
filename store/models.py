from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length =250,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)   
    #the url with which a category is accessed