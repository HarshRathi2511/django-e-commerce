from django.forms import ModelForm
from store.models import Product

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['title','price','category','description','image','stock','in_stock']