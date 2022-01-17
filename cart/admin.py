from django.contrib import admin
from .models import OrderItem,Order, WishlistItem
from import_export import resources
from .models import OrderItem,Order
from import_export.admin import ImportExportModelAdmin



#registering the import export model
# @admin.register(OrderItem)
# class OrderAdmin(ImportExportModelAdmin):
#     list_display= ('item','quantity','user','vendor','ordered')

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(WishlistItem)


