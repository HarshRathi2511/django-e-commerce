from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from cart.models import Order, OrderItem
from store.models import Product
from user.models import Address
from .forms import CustomUserCreationForm, ProfileUpdateForm, ReviewForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# def profile(request):
#   # when a profile returns data from the post request then it is accesed in the same view using the request.Methof
#      if request.method == 'POST':  #what to run after the information is posted and we passed in the new data 
#       #  instances to know what profiles to update 
#       # request.FILES gets the file data from the user 
#       # request.POST is the post data the user updates 
#           p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#           # populate the forms with the data collected from the user 
#           if p_form.is_valid():        
#             p_form.save()
#             messages.success(
#               request, f'Your profile has been updated ')
#           # redirect them to the profile page after creating the account
#             return redirect('profile')
#      else: 
#            p_form = ProfileUpdateForm(instance=request.user.profile)

#      context = {
#       'p_form':p_form,
#      }
#      return render(request,'user/profile.html',context) 

def profile(request):
    orders_by_user= Order.objects.filter(user=request.user,ordered=True)
    context={
        'total_orders':orders_by_user
    }
    return render(request,'user/profile.html',context)

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        f = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': f})


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['apartment', 'street', 'city', 'country', 'pin', ]
    template_name = 'user/register_address.html',
    success_url='/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateUserAddress(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    # Deny a request with a permission error if the test_func() method returns False.
    model = Address
    fields=['apartment','street','city','country','pin',]
    template_name='user/update_user_address.html',
    success_url = '/cart/order-summary'

    def test_func(self):
        address = self.get_object() #Return the object the view is displaying.  
        if self.request.user ==address.user:
            return True
        return False   

    def form_valid(self,form) :  #(method) form_valid: (self: Self@PostUpdateView, form) -> HttpResponse
        form.instance.user =self.request.user
        return super().form_valid(form)    
    

@login_required
def write_review(request,slug):
    if request.method=='POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            #not yet put the changes to the database ,otherwise crash
            review= form.save(commit=False )
            #add the user 
            review.user= request.user
            #add the product
            product= get_object_or_404(Product,slug=slug)
            review.product= product
            #add the order_item 
            order_item= get_object_or_404(OrderItem,item= product)
            review.order_item = order_item
            review.save()
            messages.info(request,'Your review has been added successfully')
            return redirect('profile')
    else:
        form =ReviewForm()        
    return render(request,'user/write-review.html',{'form':form})    