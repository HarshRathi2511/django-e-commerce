from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from user.models import Address
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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

class AddressCreateView(LoginRequiredMixin,CreateView):
    model = Address
    fields=['apartment','street','city','country','pin',]
    template_name='user/register_address.html'

    def form_valid(self,form) :  
        form.instance.user =self.request.user
        return super().form_valid(form)