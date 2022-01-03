from django.urls import path
from .import views 

app_name = 'store'

urlpatterns = [
    path('',views.home_products,name= 'home_products'), 
    path('grocery/<slug:slug>',views.product_detail,name= 'product_detail')
    # <slug:slug> => var and the name 
]
