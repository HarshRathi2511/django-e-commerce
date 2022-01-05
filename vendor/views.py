from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from cart.models import OrderItem, Order
from user.models import Address
from store.models import Product
from .models import Vendor
from django.views.generic import DetailView,CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from .forms import ProductForm

from django.utils.text import slugify


# class VendorRegisterView(LoginRequiredMixin, CreateView):
#     model = Vendor
#     fields = ['shop_name']
#     template_name = 'vendor/register.html',
#     success_url='vendor:vendor-profile'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
     


@login_required
def add_product(request):
    if request.method=='POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            #not yet put the changes to the database ,otherwise crash
            product= form.save(commit=False )
            #add the vendor
            product.created_by=request.user.vendor
            #add the slug
            product.slug= slugify(product.title)
            #commit the changes to the DB
            product.save()
            messages.info(request,'Your product has been added successfully')
            return redirect('vendor:vendor-profile')
    else:
        form =ProductForm()        
    return render(request,'vendor/add_product.html',{'form':form})

@login_required
def delete_product(request,slug):
    product= get_object_or_404(Product,slug=slug)
    product.delete()
    messages.info(request,'Your product has been deleted')
    return redirect('vendor:vendor-profile')

class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Product
    fields=['title','price','category','description','image','in_stock']

    def form_valid(self,form) :
        form.instance.created_by =self.request.user       
        return super().form_valid(form)
        
    #to ensure that the vendor only updates his created product    
    # def test_func(self):
    #     product = self.get_object() #Return the object the view is displaying.  
    #     if product.created_by.user == self.request.user:
    #         return True
    #     return False        



def become_vendor(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            #pre built login function
            login(request,user)
          
            vendor = Vendor.objects.create(shop_name= user.username,created_by =user)

            return redirect('store:home_products')
    else:
        form =UserCreationForm()        
    return render(request,'vendor/register.html',{'form':form})


@login_required
def vendor_profile(request):
    # vendor = get_object_or_404(Vendor,created_by=request.user)
    vendor = request.user.vendor
    products= vendor.products.all()
    context={
        'vendor':vendor,
        'products':products
    }
    return render(request,'vendor/profile.html',context)   