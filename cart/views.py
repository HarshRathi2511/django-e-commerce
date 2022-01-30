from fileinput import filename
import re
from django.http import HttpResponse
from urllib import response
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import View
# from cart.emails import notify_customer, notify_vendor
from cart.models import OrderItem, Order
import user
from user.models import Profile, UserDetail
from user.views import profile
from vendor.models import Vendor
from .models import Product, WishlistItem
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from tablib import Dataset
# Create your views here.


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        #add checks 
        try:
            if Vendor.objects.filter(created_by=request.user).exists:
                messages.info(request,'Vendors cant buy!')
                return render('store:product_detail')
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
    if Vendor.objects.filter(created_by=request.user).exists:
        messages.info(request,'Vendors cant add products in cart')
        return render('store:product_detail')
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
        #  messages.info(request,'Please add the shipping address by updating your profile')
         return False    

#change the balance and the stock quantity
#final checkout and set the order 
# @user_passes_test(isAddress)
@login_required
def final_checkout(request):
    #don't let the vendor order be able order stuff
    # if request.user.vendor:
    #     messages.info(request,'Vendors cant order from this site !!!')
    #     return redirect('cart:order-summary')

    #checks before shipping out 
    user_detail =UserDetail.objects.get(user=request.user)

    if not user_detail.address:
        messages.info(request,'Please fill an address before continuing')
        return redirect('cart:order-summary')

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    #amount spend by the user 
    if order_qs.exists():       
        order_qs.update(ordered=True)     
        
        #get the most recent order 
        order = Order.objects.order_by('ordered_date').filter(user=request.user,ordered=True).last()
        #update the balance in the users account 
        total_amount_in_cart= order.get_total_price_of_cart()
        profile_balance= get_object_or_404(Profile,user=request.user)

        #check if the user has balance 
        if profile_balance.balance <= total_amount_in_cart:
            messages.info(request,'You do not have enough money in the cart !')
        else:               
            profile_balance.balance= profile_balance.balance- total_amount_in_cart
            profile_balance.save(update_fields=['balance'])  # more efficient instead of updating the whole model row 
            messages.info(request,f'Deducted {total_amount_in_cart} from your balance!')


        # get the order_items in the order set 
        order_list = order.items.all()
        for order_item in order_list:
            #decrease the stock of the product
            order_item.item.decrease_stock(order_item.quantity)
                # print(order_item.user)
                #send emails to the vendor as there are many vendors in an order_query_Set 
                # notify_vendor(order_item)

        #finally notify the customer by passing in the latest order 
        # notify_customer(order)        
        
        messages.info(request,'Your order has been placed and a confirmation email has been sent !')

          
    else:
        messages.info(request,'Something went wrong !')      

    return redirect('store:home_products')    



#WISHLIST FUNCTIONS 
@login_required
def wishlist(request):
    wishlist_items =WishlistItem.objects.filter(user=request.user)
    context= {'items': wishlist_items}
    return render(request,'cart/wishlist.html',context)

@login_required
def add_to_wishlist(request,slug):
    product= get_object_or_404(Product,slug=slug)
    vendor = product.created_by
    WishlistItem.objects.create(item=product,user=request.user,vendor=vendor)
    messages.info(request,'Item put in wishlist !')
    return redirect('store:home_products') 

@login_required
def remove_from_wishlist(request,slug):
    product= get_object_or_404(Product,slug=slug)
    vendor = product.created_by
    WishlistItem.objects.filter(item=product,user=request.user,vendor=vendor).delete()
    messages.info(request,'Item removed from wishlist !')
    return redirect('cart:wishlist') 


# #exporting importing from the admin locations
# def export_data(request):
#     if request.method == 'POST':
#         # Get selected option from form
#         file_format = request.POST['file-format']
#         order_resource = OrderResource()
#         dataset = order_resource.export()
#         if file_format == 'CSV':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
#             return response        
#         elif file_format == 'JSON':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
#             return response
#         elif file_format == 'XLS (Excel)':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
#             return response   
#     return render(request, 'cart/export_import_data_page.html') 


# def upload_order(request):
#     if request.method=='POST':
#         order_resource= OrderResource()
#         dataset= Dataset()

#         new_order= request.FILES['myfile']


#         #messages for wrong format excel 
#         imported_data = dataset.load(new_order.read(),format='xlsx')

#         for data in imported_data:
#             order = OrderItem(data[0],data[1],data[2],data[3],data[4],data[5])
#             order.save()

#     return render(request,'cart/import_data.html',)        


