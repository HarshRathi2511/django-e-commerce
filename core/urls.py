"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    # path('profile/',user_views.profile,name='profile'),
    path('register/',user_views.register,name='register'),


    #path for address 
    path('register-address/',user_views.AddressCreateView.as_view(),name ='register-address'),
    path('update-address/<int:pk>',user_views.UpdateUserAddress.as_view(),name ='update-address')

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
