from django.contrib import admin
from .models import  Profile, Review, UserDetail
# Register your models here.

admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(UserDetail)