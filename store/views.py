from django.shortcuts import render
from .models import Category,Product

# Create your views here.
def home_products(request):   #HttpRequest instance 
    print(request.method)
    products = Product.objects.all()
    return render(request,'store/home.html',{'products':products})

    #render returns an HttpResponse while request is an HttpRequest class