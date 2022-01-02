from django.contrib import admin
from .models import Product,Category
# Register your models here.

# admin.site.register(Category)
# admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields={'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','slug','price','category','created_by']    #how the item is showed in the list 
    list_filter=['in_stock']
    prepopulated_fields={'slug':('title',)}    