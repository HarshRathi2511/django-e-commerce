from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from cart.models import OrderItem,Order
from .models import Category,Product
from django.views.generic import DetailView
# Create your views here.

def cart_summary(request):
    return render(request,'cart/summary.html')


#slug is the product slug 
def add_to_cart(request,slug):
    #get the product and create the order item 
    product= get_object_or_404(Product,slug=slug)
    order_item = OrderItem.objects.create(item=product)
    #check if the user is the logged in user and were only getting orders thats not completed
    # as a user can have many orders 
    order_query_set = Order.objects.filter(user=request.user,ordered=False)
    
    if order_query_set.exists():

        #need to make it so that only one order is placed at a time
        order = order_query_set[0]
        #check if the order item is in the cart as we can delete and add items in the cart 
        if order.items.filter(item__slug= product.slug).exists():
            order_item.quantity+=1
            
            order_item.save()
        else:
            order.items.add(order_item)    

    #create a new order 
    else:
        ordered_date= timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)  

    return redirect('store:product_detail',slug=slug)    

        