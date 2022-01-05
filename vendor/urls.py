from django.urls import path
from .import views 

app_name = 'vendor'

urlpatterns = [
    path('become-vendor/',views.become_vendor,name='become-vendor'),    
    path('profile/',views.vendor_profile,name='vendor-profile'),  
    path('new-product',views.ProductCreateView.as_view(template_name = 'vendor/new-product.html'),name='new-product') ,
    path('update-product/<slug:slug>',views.ProductUpdateView.as_view(template_name = 'vendor/update-product.html'),name='update-product') 
]
