from django.urls import path
from .import views 

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<slug:slug>',views.add_to_cart,name= 'add-to-cart'), 
    path('remove-from-cart/<slug:slug>',views.remove_from_cart,name= 'remove-from-cart'), 
    path('order-summary',views.OrderSummaryView.as_view(),name='order-summary'),
    path('remove-single-item-from-cart/<slug:slug>',views.remove_single_item_from_cart,name ='remove-single-item-from-cart'),
    path('add-single-item-to-cart/<slug:slug>',views.add_single_item_to_cart,name ='add-single-item-to-cart'),
    path('final-checkout',views.final_checkout,name='final-checkout'),

    #wishlist 
    path('add-to-wishlist/<slug:slug>',views.add_to_wishlist,name= 'add-to-wishlist'), 
    path('wishlist',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<slug:slug>',views.remove_from_wishlist,name= 'remove-from-wishlist'), 

    #import export 
    path('export-data/', views.export_data, name="export_data"),
]
