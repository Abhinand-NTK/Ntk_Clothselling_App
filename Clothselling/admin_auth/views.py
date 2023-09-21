from .models import Product, Brand, Subcategory
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
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

    if 'user' in request.session:
        return redirect('user_login')

    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        admin = authenticate(email=email, password=password)

        if admin and admin.is_superuser:
            if not admin.is_blocked:
                login(request, admin)
                request.session['admin'] = email
                return redirect('admindashboard')
            else:
                logout_admin()
                # return redirect('adminlogin')
        else:
            return HttpResponse('oops')

    return render(request, "adminpanel/adminlogin.html")


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admindashboard(request):
    return render(request, 'adminpanel/admindashboard.html')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminusers(request):

    users = CustomUser.objects.filter(is_superuser=False)
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/adminusers.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminproducts(request):
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    product = Product.objects.all()
    context = {'brand': brand, 'subcategory': subcategory, 'product': product}
    return render(request, 'adminpanel/adminproducts.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminaddproducts(request):
    if request.method == 'POST':

        productname = request.POST['productName']
        description = request.POST['description']
        brand_id = request.POST['brand']
        subcategory_id = request.POST['subcategory']
        men = request.POST.get('men', 'False') == 'True'
        woman = request.POST.get('woman', 'False') == 'True'
        kids = request.POST.get('kids', 'False') == 'True'
        combos = request.POST.get('combos', 'False') == 'True'
        images = request.FILES.get('image')
        brand = Brand.objects.get(id=brand_id)
        subcategory = Subcategory.objects.get(id=subcategory_id)

        if images:
            try:
                imag = Product(name=productname, description=description, brand=brand,
                               subcategory=subcategory, men=men, kids=kids, woman=woman, combos=combos, images=images)
                imag.save()
                messages.success(request, "Procduct added sucessfully")
            except IntegrityError:
                pass

        return redirect('adminproducts')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminproductsvarients(request):

    if request.method == 'POST':
        # try:
        product_id = request.POST.get('product')
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if product_id and size_id and color_id and price and stock:
            product = Product.objects.get(id=product_id)
            color = Color.objects.get(id=color_id)
            size = Size.objects.get(id=size_id)
            product_variant = ProductVariant(
                product=product,
                color=color,
                size=size,
                price=price,
                stock=stock,
            )
            product_variant.save()

            multiple_images = request.FILES.getlist('image', None)
            if multiple_images:  # Use getlist to get multiple files
                for image in multiple_images:
                    photos = Multipleimges.objects.create(
                        product=product_variant,
                        images=image,
                    )
                    # photos.save()

            messages.success(request, "Product added successfully")
            return redirect('productvarients')

        # except IntegrityError:
        # messages.error(request, "Error adding product")
        # return redirect('productvarients')

    products = Product.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    variants = ProductVariant.objects.all()
    images = Multipleimges.objects.all()  # Retrieve all images
    context = {'products': products, 'colors': colors,
               'sizes': sizes, 'variants': variants, 'images': images}
    return render(request, 'adminpanel/adminproducts_varient.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admineditproductsvarients(request, id):
    product_id = None
    size_id = None
    color_id = None

    if request.method == 'POST':
        product_id = request.POST['product']
        size_id = request.POST['size']
        color_id = request.POST['color']
        price = request.POST['price']
        stock = request.POST['stock']
        images = request.FILES.get('image')

        try:
            if product_id is not None:
                product = Product.objects.get(id=product_id)
                color = Color.objects.get(id=color_id)
                size = Size.objects.get(id=size_id)
                product_v = ProductVariant(
                    id=id, product=product, color=color, size=size, price=price, stock=stock, images=images)
                product_v.save()
                return redirect('productvarients')

        except IntegrityError:
            pass

    return redirect('productvarients')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admineditproducts(request, id):

    from django.shortcuts import render, redirect


def admineditproducts(request, id):

    if request.method == 'POST':
        productname = request.POST['productName']
        description = request.POST['description']
        brand_id = request.POST['brand']
        subcategory_id = request.POST['subcategory']
        men = request.POST.get('men', False)
        woman = request.POST.get('woman', False)
        kids = request.POST.get('kids', False)
        combos = request.POST.get('combos', False)
        images = request.FILES.get('image')

        subcategory = Subcategory.objects.get(id=subcategory_id)
        brand = Brand.objects.get(id=brand_id)

        # Retrieve the product object to update
        product = Product.objects.get(id=id)

        # Update the attributes
        product.name = productname
        product.description = description
        product.brand = brand
        product.subcategory = subcategory
        product.men = men
        product.woman = woman
        product.kids = kids
        product.combos = combos

        if images:
            product.images = images

        product.save()

        return redirect('adminproducts')  # Redirect to the appropriate URL

    # return render(request, 'your_template.html')  # Replace with your template name


def list_unlist_products(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        message = request.POST['check']
        product = Product.objects.get(id=product_id)
        if message == "true":  # Corrected typo from "ture" to "true"
            product.active = True
        else:
            product.active = False
        product.save()
        return redirect('adminproducts')


def list_unlist_products_vareints(request):
    if request.method == 'POST':
        product_id = request.POST['product__vareint_id']
        message = request.POST['check']
        product_varient = ProductVariant.objects.get(id=product_id)
        if message == "true":  # Corrected typo from "ture" to "true"
            product_varient.is_avaliable = True
        else:
            product_varient.is_avaliable = False
        product_varient.save()
        return redirect('productvarients')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admincategory(request):
    cat = Category.objects.all()
    print(cat)
    context = {
        'cat': cat,
    }
    subcat = Subcategory.objects.all()
    print(subcat)
    context1 = {
        'subcat': subcat,
    }
    mer = {**context, **context1}
    return render(request, 'adminpanel/admincateogry.html', mer)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def listsubcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('id_S')
        message = request.POST.get('check')
        subcategory = Subcategory.objects.get(id=subcategory_id)

    if message == "true":
        subcategory.active = True
    elif message == "false":
        subcategory.active = False

    subcategory.save()
    return redirect('category')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def listcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        message = request.POST.get('check')
        category = Category.objects.get(id=category_id)

        if message == "true":
            category.active = True
        elif message == "false":
            category.active = False

        category.save()
        return redirect('category')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            try:
                existing_category = Category.objects.filter(name=name).first()

                if existing_category is None:

                    category = Category(name=name)

                    category.save()
                    messages.success(request, 'Category added')
                else:
                    messages.error(request, 'Already existing the category')
            except IntegrityError:
                # Handle unique constraint violation if necessary
                pass
        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def editcategory(request, id):
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
                existing_subcategory = Subcategory.objects.filter(
                    category=category, name=name).first()

                if existing_subcategory is None:
                    subcategory = Subcategory(category=category, name=name)
                    subcategory.save()
                    messages.success(request, 'Subcategory added successfully')
                else:
                    messages.warning(
                        request, 'Subcategory already exists for this category')
            except IntegrityError:
                # Handle unique constraint violation if necessary
                messages.error(
                    request, 'An error occurred while adding the subcategory')

        return redirect('category')  # Redirect to the appropriate URL

    return redirect('category')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def editsubcategory(request, id):
    # # subcategory = get_object_or_404(Subcategory, id=id)
    # def editsubcategory(request, id):
    subcategory = Subcategory.objects.get(id=id)

    if request.method == 'POST':
        category_id = request.POST['selectedCategory']
        name = request.POST['name']

        if name:
            try:
                category = get_object_or_404(Category, id=category_id)

                # Check if the new name already exists in the selected category
                existing_subcategory = Subcategory.objects.filter(
                    category=category, name=name).exclude(id=id).first()
                if existing_subcategory is None:
                    # Update the subcategory's category and name
                    subcategory.category = category
                    subcategory.name = name
                    subcategory.save()
                else:
                    pass
                    # Handle the case where the name already exists in the category
                    # You might want to provide an error message or take appropriate action

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
            messages.error(
                request, 'Plese select a brand and image for the brand')

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


def logout_admin(request):
    logout(request)
    if 'admin' in request.session:
        del request.session['admin']
    return redirect('adminlogin')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admin_user_list_unlist(request):
    if 'admin'in request.session:
        if request.method == 'POST':
            user_id = request.POST['user_id']
            message = request.POST['check']
            user = CustomUser.objects.get(id=user_id)

        if message == 'true':
            user.is_blocked = True
        else:
            user.is_blocked = False
        user.save()
        return redirect('adminusers')
