from django.shortcuts import render
from admin_auth.models import *

# Create your views here.

def home(request):

    products=Product.objects.all()[:9]
    productsvarient=ProductVariant.objects.all()
    context={
            'products':products
             }

    return render(request,"home.html",context)

