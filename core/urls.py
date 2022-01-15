#MAKE IT SO THAT CATEGORY AND PRODUCT ARE NOT FOREIGN KEY RELATED 

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from  django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    #path for store 
    path('',include('store.urls',namespace='store',)),

    #path for cart and orders 
    path('cart/',include('cart.urls',namespace='cart')),
    
    #paths for registering,login,logout,profile 

    #custom views that django gives us for logging in and logging out 
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),  #class based views 
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'),name='logout'),
    path('profile/',user_views.profile,name='profile'),
    path('register/',user_views.register,name='register'),


    #path for address 
    path('register-address/',user_views.add_address,name ='register-address'),
    path('update-address/',user_views.update_address,name ='update-address') ,

    #path for vendors 
    path('vendor/',include('vendor.urls',namespace='vendor')),

    #reviews 
    path('write-review/<slug:slug>',user_views.write_review,name='write-review'),

    #add balance to profile
    path('add-balance',user_views.add_balance,name='add-balance'),
    path('update-balance',user_views.update_balance,name='update-balance'),

    #oauth urls 
    path('accounts/',include('allauth.urls')),
    
    #login redirect vieews
    path('login-redirect/',user_views.login_redirect_view,name='login-redirect'),
    
]









# Using namespace in the include() allows you to include the same app more than once, with a different 
# namespace for each instance.

# Auto-add the applications.
# for app in settings.LOCAL_APPS:
#     urlpatterns += patterns('',
#         url(r'^{0}/'.format(app), include(app + '.urls', namespace=app)),
#     )
if settings.DEBUG:  # allows the static files to work in the browser
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
