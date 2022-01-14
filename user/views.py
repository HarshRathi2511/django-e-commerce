from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import fields
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from cart.models import Order, OrderItem
from store.models import Product
from user.models import  Profile, UserDetail
from .forms import CustomUserCreationForm, ProfileForm, ReviewForm, UserAddressForm

def profile(request):
    orders_by_user= Order.objects.filter(user=request.user,ordered=True).order_by('-ordered_date')
    user_detail = get_object_or_404(UserDetail,user=request.user)
    form = UserAddressForm(instance=user_detail)
    profile_balance= get_object_or_404(Profile,user=request.user)
    
    context={
        'total_orders':orders_by_user,
        'user_detail':user_detail,
        'form':form,
        'profile_balance':profile_balance
        
    }
    return render(request,'user/profile.html',context)

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            user= f.save()
            UserDetail.objects.create(user=user)
            Profile.objects.create(user=user)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        f = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': f})   

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

def add_address(request):
    if request.method=='POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Your address has been added')
    else:
        form=UserAddressForm()
    return render(request,'user/register_address.html',{'form':form})            

def update_address(request):
    user_detail = get_object_or_404(UserDetail,user=request.user)
    if request.method=='POST':
        form= UserAddressForm(request.POST,instance=user_detail)  
        if form.is_valid():
            form.save()
            messages.info(request,'Your address has been updated')
            return redirect('profile')

    else:
        form=UserAddressForm(instance=user_detail)
    return render(request,'user/update_user_address.html',{'form':form}) 


