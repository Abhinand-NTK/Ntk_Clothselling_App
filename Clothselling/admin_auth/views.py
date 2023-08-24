from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponse
from admin_auth.models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_control

# Create your views here.
def adminlogin(request):

    if request.method=="POST":
        email=request.POST['username']
        password=request.POST['password']

       

        admin=authenticate(email=email,password=password)
        
        if admin:
         if admin.is_superuser:
            login(request, admin)
            return redirect('admindashboard')
        else:
            return HttpResponse('oops')



      
    return render(request,"adminpanel/adminlogin.html")


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admindashboard(request):
    return render(request,'adminpanel/admindashboard.html')


@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def adminusers(request):

    users=CustomUser.objects.all()
    context={
        'users':users,
        }
    return render(request,'adminpanel/adminusers.html',context)


@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def adminproducts(request):
    brand=Brand.objects.all()
    subcategory=Subcategory.objects.all()
    product=Product.objects.all()
    context={'brand': brand,'subcategory':subcategory,'product':product}
    return render(request,'adminpanel/adminproducts.html',context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminaddproducts(request):
    if request.method=='POST':

     
        productname=request.POST['productName']
        description=request.POST['description']
        brand_id=request.POST['brand']
        subcategory_id=request.POST['subcategory']
        images = request.FILES.get('image')
        brand=Brand.objects.get(id=brand_id)
        subcategory=Subcategory.objects.get(id=subcategory_id)

     

        if images:
                try:
                    imag=Product(name=productname,description=description,brand=brand,subcategory=subcategory,images=images)
                    imag.save()
                except IntegrityError:
                    pass

        return redirect('adminproducts')
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminproductsvarients(request):
    product_id = None
    size_id = None
    color_id = None

    if request.method == 'POST':
        product_id = request.POST['product']
        size_id = request.POST['size']
        color_id = request.POST['color']
        price = request.POST['price']
        stock = request.POST['stock']

        try:
            if product_id is not None:
                product = Product.objects.get(id=product_id)
                color = Color.objects.get(id=color_id)
                size = Size.objects.get(id=size_id)
                product_v = ProductVariant(product=product, color=color, size=size, price=price, stock=stock)
                product_v.save()
                return redirect('productvarients')

        except IntegrityError:
             pass    

    products=Product.objects.all()
    size=Size.objects.all()
    color=Color.objects.all()
    varient=ProductVariant.objects.all()
    context={'products':products,'color':color,'size':size,'varient':varient}
    return render(request,'adminpanel/adminproducts_varient.html',context)
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admineditproductsvarients(request,id):
    product_id = None
    size_id = None
    color_id = None

    if request.method == 'POST':
        product_id = request.POST['product']
        size_id = request.POST['size']
        color_id = request.POST['color']
        price = request.POST['price']
        stock = request.POST['stock']

        try:
            if product_id is not None:
                product = Product.objects.get(id=product_id)
                color = Color.objects.get(id=color_id)
                size = Size.objects.get(id=size_id)
                product_v = ProductVariant(id=id,product=product, color=color, size=size, price=price, stock=stock)
                product_v.save()
                return redirect('productvarients')

        except IntegrityError:
             pass    

  
    return redirect('productvarients')

@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admineditproducts(request,id):

    if request.method=='POST':

        productname=request.POST['productName']
        description=request.POST['description']
        brand_id=request.POST['brand']
        subcategory_id=request.POST['subcategory']
        images = request.FILES.get('image')
        brand=Brand.objects.get(id=brand_id)
        subcategory=Subcategory.objects.get(id=subcategory_id)

        if images:
                try:
                    imag=Product(id=id,name=productname,description=description,brand=brand,subcategory=subcategory,images=images)
                    imag.save()
                except IntegrityError:
                    pass
    return redirect('adminproducts')
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admincategory(request): 
    cat=Category.objects.all()
    print(cat)
    context={
        'cat':cat,
    }
    subcat=Subcategory.objects.all()
    print(subcat)
    context1={
        'subcat':subcat,
    }
    mer={**context,**context1}
    return render(request,'adminpanel/admincateogry.html',mer)

@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)  
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            try:
                existing_category=Category.objects.filter(name=name).first()

                if existing_category is None:

                    category = Category(name=name)
                
                    category.save()
                    messages.success(request,'Category added')
                else:
                    messages.error(request,'Already existing the category')
            except IntegrityError:
                # Handle unique constraint violation if necessary
                pass
        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category') 
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True) 
def editcategory(request,id):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            try:
                category = Category(
                                    id=id,
                                    name=name
                                    )
                category.save()
                # d=Category.objects.all().delete()

            except IntegrityError:
                # Handle unique constraint violation if necessary
                pass
        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category') 

@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def addsubcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('selectedCategory')
        name = request.POST.get('name')

        if name:
            try:
                category = get_object_or_404(Category, id=category_id)
                existing_subcategory = Subcategory.objects.filter(category=category, name=name).first()

                if existing_subcategory is None:
                    subcategory = Subcategory(category=category, name=name)
                    subcategory.save()
                    messages.success(request, 'Subcategory added successfully')
                else:
                    messages.warning(request, 'Subcategory already exists for this category')
            except IntegrityError:
                # Handle unique constraint violation if necessary
                messages.error(request, 'An error occurred while adding the subcategory')

        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category')

@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def editsubcategory(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)

    if request.method == 'POST':
        category_id = request.POST['selectedCategory']
        name = request.POST['name']
        
        if name:
            try:
                category = get_object_or_404(Category, id=category_id)
                existing_subcategory = Subcategory.objects.filter(category=category, name=name).first()    
                if existing_subcategory is None:
                        subcategory = Subcategory(category=category, name=name)
                        subcategory.save()

            except IntegrityError:
                # Handle unique constraint violation if necessary
                pass

        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category')
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def addcolor_size(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        size = request.POST.get('size')
        brand_name = request.POST.get('brand')
        brand_image = request.FILES.get('image')

        if color:
            try:
                col = Color(name=color)
                col.save()
            except IntegrityError:
                pass

        if size:
            try:
                siz = Size(name=size)
                siz.save()
            except IntegrityError:
                pass

        if brand_name and brand_image:
            try:
                brand = Brand(name=brand_name, image=brand_image)
                brand.save()
                # Brand.objects.all().delete()
            except IntegrityError:
                pass
        else:
            messages.error(request,'Plese select a brand and image for the brand')

        return redirect('addcolorsize')

    colo = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()

    context = {
        'colo': colo,
        'sizes': sizes,
        'brands': brands,
    }


    return render(request, 'adminpanel/aminsizecolor.html', context)
@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def edit_color_size(request, id):
    if request.method == 'POST':
        color = request.POST.get('color')
        size = request.POST.get('size')

        if color:
            try:
                existing_color = Color.objects.get(id=id)
                existing_color.name = color
                existing_color.save()
            except Color.DoesNotExist:
                pass

        if size:
            try:
                existing_size = Size.objects.get(id=id)
                existing_size.name = size
                existing_size.save()
            except Size.DoesNotExist:
                pass

        return redirect('addcolorsize')  # Redirect after processing

    return redirect('addcolorsize')
def logout(request):
    logout(request)


