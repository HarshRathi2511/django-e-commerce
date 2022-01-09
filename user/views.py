from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from cart.models import Order, OrderItem
from store.models import Product
from user.models import Address, Profile
from .forms import CustomUserCreationForm, ProfileForm, ReviewForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


 

def profile(request):
    orders_by_user= Order.objects.filter(user=request.user,ordered=True)
    profile = get_object_or_404(Profile,user=request.user)
    
    context={
        'total_orders':orders_by_user,
        'profile':profile,
        
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

@login_required
def add_balance(request):
    if request.method=='POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user= request.user
            money_added= form.cleaned_data['balance']
            messages.info(request,f"Added {money_added} dollars to your account !!")
            profile.save()
            return redirect('profile')
    
    else:
        form=ProfileForm()

    return render(request,'user/balance.html',{'form':form})  


@login_required
def update_balance(request):
    profile = get_object_or_404(Profile,user=request.user)
    if request.method=='POST':
        form= ProfileForm(request.POST,instance=profile)  
        if form.is_valid():
            form.save()
            messages.info(request,'Your balance has been updated')
            return redirect('profile')

    else:
        form=ProfileForm(instance=profile)
    return render(request,'user/update-balance.html',{'form':form})      

    




