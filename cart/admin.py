from django.contrib import admin
from .models import OrderItem,Order, WishlistItem
from import_export import resources
from .models import OrderItem,Order
from import_export.admin import ImportExportModelAdmin

class OrderResource(resources.ModelResource):
    class Meta:
        model=OrderItem
        fields = ('item','quantity','user','vendor','ordered')

#registering the import export model
class OrderAdmin(ImportExportModelAdmin):
    pass

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(WishlistItem)


