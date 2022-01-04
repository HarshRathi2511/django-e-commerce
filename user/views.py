from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from user.models import Address
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
    
    