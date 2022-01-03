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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls',namespace='store',)),
    path('cart/',include('cart.urls',namespace='cart')),
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
