from django.shortcuts import get_object_or_404, render
from .models import Category,Product
from django.views.generic import DetailView


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

def product_detail(request,slug):
    product= get_object_or_404(Product,slug=slug,in_stock=True)
    return render(request,'store/detail.html',{'product':product})
    # Alternative to 404
    #  try:
    #       return Record.objects.get(id=self.request.query_params['id'])
    #     except Record.DoesNotExist:
    #       raise Http404()