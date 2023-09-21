from django.shortcuts import render
from admin_auth.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):

    products=Product.objects.all().order_by('-id')[:8]
    productsvarient=ProductVariant.objects.all()
    context={
            'products':products
             }

    return render(request,"home.html",context)
def product_category(request):

    return render(request,'category_management_userside.html')
def Womans(request):
    products=Product.objects.filter(woman=True,men=False,combos=False,kids=False)
    context={'products':products}
    return render(request,"category_management_userside.html",context)
def Mens(request):
    products=Product.objects.filter(woman=False,men=True,combos=False,kids=False)
    context={'products':products}
    return render(request,"category_management_userside.html",context)
def kids(request):
    products=Product.objects.filter(woman=False,men=False,combos=False,kids=True)
    context={'products':products}
    return render(request,"category_management_userside.html",context)
def combos(request):
    products=Product.objects.filter(woman=False,men=False,combos=True,kids=False)
    context={'products':products}
    return render(request,"category_management_userside.html",context)
def product_details(request,id):

    product = get_object_or_404(Product, id=id)
    product_variants = ProductVariant.objects.filter(product=product)
    images = Multipleimges.objects.filter(product__in=product_variants)

    context = {'product': product, 'product_variants': product_variants, 'images': images}
    # return render(request, 'products_details.html', context)
    # variant_images = [variant.images for variant in p]
    # context = {'variant_images': variant_images}

    # product=Product.objects.get(id=id)
    # product_vareint=ProductVariant.objects.filter(product=product)
    # product_vareint_data=[]
    # for varient in product_vareint:
    #     varient_data={
    #         'color' : varient.color,
    #         'price' : varient.price,
    #         'images' : varient.images,
    #     }
    #     product_vareint_data.append(varient_data)
    # context={'product_vareint':product_vareint_data}

    # product=Product.objects.all()
    # product_vareint=ProductVariant.objects.all()

    return render(request,'products_detalils.html',context)


