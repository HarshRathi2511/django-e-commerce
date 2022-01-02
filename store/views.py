from django.shortcuts import render
from .models import Category,Product


def categories(request): #make this accessible in every template 
    #register this view in settings.py
    return {
        'categories':Category.objects.all()
    }
# Create your views here.
def home_products(request):   #HttpRequest instance 
    print(request.method)
    products = Product.objects.all()
    return render(request,'store/home.html',{'products':products})
    #render returns an HttpResponse while request is an HttpRequest class