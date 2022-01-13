from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import View
from cart.models import OrderItem, Order
from user.models import Profile, UserDetail
from .models import Product, WishlistItem
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        #add checks 
        try:
            orders = Order.objects.get(user=self.request.user,ordered=False)
            user_detail=get_object_or_404(UserDetail,user=self.request.user)
            context={'orders':orders,'user_detail':user_detail}
            return render(self.request,'cart/order_summary.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have any active items in the cart")
            return redirect('store:home_products')    

# TWO WAYS OF REDIRECTING :-
# (login_url='/example url you want redirect/') #redirect when user is not logged in   
# Change LOGIN_URL in settings.py          
@login_required
def add_to_cart(request, slug):
    # get the product and create the order item
    product = get_object_or_404(Product, slug=slug)
    # do not create new order item if it already in cart
    vendor = product.created_by
    order_item, created = OrderItem.objects.get_or_create(
        item=product, user=request.user, ordered=False,vendor=vendor)
    # check if the user is the logged in user and were only getting orders thats not completed
    # as a user can have many orders
    order_query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query_set.exists():

        # need to make it so that only one order is placed at a time
        order = order_query_set[0]
        # check if the order item is in the cart as we can delete and add items in the cart
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            messages.info(request, "Item quantity was updated")
            order_item.save()
            return redirect('store:product_detail', slug=slug)
        else:
            messages.info(request, "Item added to cart")
            order.items.add(order_item)
            return redirect('store:product_detail', slug=slug)

    # create a new order
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart")
        return redirect('store:product_detail', slug=slug)


# SOME STUPID BUG HERE 
@login_required
def remove_from_cart(self, slug):
    item = get_object_or_404(Product, slug=slug)
    vendor = item.created_by
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False,
                    vendor=vendor
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
                return redirect('store:product_detail', args=[slug])
            else:
                messages.info(request, "This item was not in your cart")
                return redirect('store:product_detail', args=[slug])
    else:
            messages.info(request, "You do not have an active order")
            return redirect('store:product_detail', args=[slug])

    # return redirect('store:product_detail', args=[slug])



@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    vendor=item.created_by
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
                vendor=vendor
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart:order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:order-summary")

#just for redirecting to the order summary page 
@login_required
def add_single_item_to_cart(request, slug):
    # get the product and create the order item
    product = get_object_or_404(Product, slug=slug)
    vendor=product.created_by
    # do not create new order item if it already in cart
    order_item, created = OrderItem.objects.get_or_create(
        item=product, user=request.user, ordered=False,vendor=vendor)
    # check if the user is the logged in user and were only getting orders thats not completed
    # as a user can have many orders
    order_query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query_set.exists():

        # need to make it so that only one order is placed at a time
        order = order_query_set[0]
        # check if the order item is in the cart as we can delete and add items in the cart
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            messages.info(request, "Item quantity was updated")
            order_item.save()
            return redirect("cart:order-summary")
        else:
            messages.info(request, "Item added to cart")
            order.items.add(order_item)
            return redirect("cart:order-summary")

    # create a new order
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart")
        return redirect("cart:order-summary")

def isAddress(user):
     user_detail= get_object_or_404(UserDetail,user=user)
     if user_detail.address:
         return True
     else:
         return False    

#change the balance and the stock quantity
#final checkout and set the order 
@user_passes_test(isAddress)
@login_required
def final_checkout(request):
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    #amount spend by the user 
    if order_qs.exists():       
        order_qs.update(ordered=True)     
        messages.info(request,'Your order has been placed and balance has been updated !')  
    else:
        messages.info(request,'Something went wrong !')      

    return redirect('store:home_products')    



#WISHLIST FUNCTIONS 
def wishlist(request):
    wishlist_items =WishlistItem.objects.filter(user=request.user)
    context= {'items': wishlist_items}
    return render(request,'cart/wishlist.html',context)


def add_to_wishlist(request,slug):
    product= get_object_or_404(Product,slug=slug)
    vendor = product.created_by
    WishlistItem.objects.create(item=product,user=request.user,vendor=vendor)
    messages.info(request,'Item put in wishlist !')
    return redirect('store:home_products') 

def remove_from_wishlist(request,slug):
    product= get_object_or_404(Product,slug=slug)
    vendor = product.created_by
    WishlistItem.objects.filter(item=product,user=request.user,vendor=vendor).delete()
    messages.info(request,'Item removed from wishlist !')
    return redirect('cart:wishlist') 

