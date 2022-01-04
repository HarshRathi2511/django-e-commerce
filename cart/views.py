from django.contrib import messages
from django.http import request
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import View
from cart.models import OrderItem, Order
from .models import Category, Product
from django.views.generic import DetailView
# Create your views here.


class OrderSummaryView(View):
    def get(self,*args,**kwargs):
        return render(self.request,'cart/order_summary.html')
    # model=Order
    # template_name= 'order_summary'

# def order_summary_view(request):
#       return render(request,'store/order_summary.html')
# slug is the product slug
def add_to_cart(request, slug):
    # get the product and create the order item
    product = get_object_or_404(Product, slug=slug)
    # do not create new order item if it already in cart
    order_item, created = OrderItem.objects.get_or_create(
        item=product, user=request.user, ordered=False)
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
def remove_from_cart(self, slug):
    item = get_object_or_404(Product, slug=slug)
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
                    ordered=False
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
