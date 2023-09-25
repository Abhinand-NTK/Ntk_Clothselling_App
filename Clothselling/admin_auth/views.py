from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Brand, Subcategory, Banner
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from admin_auth.models import *
from cart.models import *
from order.models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_control
from user_auth.models import *
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from order.models import Order
from django.db.models import Sum
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import json


# Create your views here.


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admindashboard(request):

    total_orders = Order.objects.all().count()
    total_revenue_data = Order.objects.filter(status='Delivered')
    total_profit_data = Order.objects.filter(status='Delivered')
    total_revenue = 0
    total_profit = 0

    for item in total_revenue_data:
        total_revenue = total_revenue + (item.paid_amount-item.tax)

    for item in total_profit_data:
        total_profit = total_profit + ((item.paid_amount-item.tax)*.2)

    Payment_Analayis = [Order.objects.filter(payment_method='Cod').count(),
                        Order.objects.filter(payment_method='Op').count(),
                        Order.objects.filter(payment_method='Wallet').count()
                        ]
    category_names = Subcategory.objects.values_list('name', flat=True)

    Category_Analysi_keys = []
    Category_Analysi_Values = []

    for category_name in category_names:
        order_products_for_category = OrderProduct.objects.filter(
            variant__product__subcategory__name=category_name
        )

        num_items_in_category = order_products_for_category.count()

        Category_Analysi_keys.append(category_name)
        Category_Analysi_Values.append(num_items_in_category)



    year_to_query = 2023


    sales_counts = (
        Order.objects
        .filter(created__year=year_to_query)
        .values('created__month')
        .annotate(sales_count=Count('id'))
        .order_by('created__month')
    )

    monthly_sales = [0] * 12

    for entry in sales_counts:
        month = entry['created__month'] - 1
        sales_count = entry['sales_count']
        monthly_sales[month] = sales_count

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(monthly_sales)
    print(monthly_sales)
    print(monthly_sales)
    print(monthly_sales)
    print(monthly_sales)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")


    Category_Analysi_keys_json = json.dumps(Category_Analysi_keys)

    response = {
        'total_orders': total_orders,
        'total_revenue_data': total_revenue,
        'total_profit_data': total_profit,
        'Payment_Analayis': Payment_Analayis,
        'Category_Analysi_keys': Category_Analysi_keys_json,
        'Category_Analysi_Values': Category_Analysi_Values,
        'monthly_sales':monthly_sales,
    }

    return render(request, 'adminpanel/admindashboard.html', response)


def Dashboard(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        print(data)
        print(data)
        print(data)
        print(data)

        start_date_orders = data.get('start_date_orders', None)
        end_date_orders = data.get('end_date_orders', None)

        print(start_date_orders)
        print(end_date_orders)

        total_orders = Order.objects.filter(
            created__range=(
                datetime.strptime(
                    data.get('start_date_orders', None), '%Y-%m-%d'),
                datetime.strptime(
                    data.get('end_date_orders', None), '%Y-%m-%d')
            ),
        ).count() if data.get('start_date_orders') else 0

        print(total_orders)

        total_revenue_data = Order.objects.filter(
            created__range=(
                datetime.strptime(
                    data.get('start_date_revenue', None), '%Y-%m-%d'),
                datetime.strptime(
                    data.get('end_date_revenue', None), '%Y-%m-%d')
            ),
            status='Delivered'
        ) if data.get('start_date_revenue') else 0

        total_revenue = -1
        if total_revenue_data != 0:
            for item in total_revenue_data:
                print("Paid Amount is this much :-", item.paid_amount)
                total_revenue = total_revenue + (item.paid_amount-item.tax)
            total_revenue = total_revenue + 1

        total_profit_data = Order.objects.filter(
            created__range=(
                datetime.strptime(
                    data.get('start_date_profit', None), '%Y-%m-%d'),
                datetime.strptime(
                    data.get('end_date_profit', None), '%Y-%m-%d')
            ),
            status='Delivered'
        )if data.get('start_date_profit') else 0

        total_profit = -1
        if total_profit_data != 0:
            for item in total_profit_data:
                total_profit = total_profit + ((item.paid_amount-item.tax)*.2)
            total_profit = total_profit + 1

        response = {
            'total_orders': total_orders,
            'total_revenue_data': total_revenue,
            'total_profit_data': total_profit

        }

        return JsonResponse(response)


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
def adminusers(request):

    users = CustomUser.objects.filter(is_superuser=False)

    per_page = 7  # You can change this to your desired number

    paginator = Paginator(users, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
    }

    return render(request, 'adminpanel/adminusers.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def adminproducts(request):
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    product_list = Product.objects.all()

    per_page = 5  # You can change this to your desired number

    paginator = Paginator(product_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'brand': brand, 'subcategory': subcategory, 'page': page}
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
        price = float(request.POST.get('price'))
        stock = float(request.POST.get('stock'))

        if product_id and size_id and color_id and price >= 0 and stock >= 0:
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

            messages.success(request, "Product Varient added successfully")
            return redirect('productvarients')
        else:
            messages.error(request, "Fill all the fields Correctly")
            return redirect('productvarients')

    products = Product.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    variants = ProductVariant.objects.all()
    images = Multipleimges.objects.all()  # Retrieve all images

    per_page = 5  # You can change this to your desired number

    paginator = Paginator(variants, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'products': products, 'colors': colors,
               'sizes': sizes, 'images': images, 'page': page}
    return render(request, 'adminpanel/adminproducts_varient.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def admineditproductsvarients(request, id):
    product_id = None
    size_id = None
    color_id = None

    if request.method == 'POST':
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
                id=id,
                product=product,
                color=color,
                size=size,
                price=price,
                stock=stock,
            )
            product_variant.save()

            multiple_images = request.FILES.getlist('image', None)

            if multiple_images:

                product_variant = ProductVariant.objects.get(id=id)
                photos = Multipleimges.objects.filter(product=product_variant)

                for image in multiple_images:
                    new_image = Multipleimges(
                        product=product_variant, images=image)
                    new_image.save()
                    photos = photos | Multipleimges.objects.filter(
                        id=new_image.id)

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

    subcat = Subcategory.objects.all()
    print(subcat)
    context1 = {
        'subcat': subcat,
    }
    per_page = 6  # You can change this to your desired number

    paginator = Paginator(subcat, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'cat': cat,
        'page': page,
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
    if 'admin' in request.session:
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


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Coupen_Management(request):

    if 'admin' in request.session:
        if request.method == 'POST':
            description = request.POST['description']
            coupon_code = request.POST['coupon_code']
            coupon_title = request.POST['coupon_title']
            discount_amount = request.POST['discount_amount']
            discount = request.POST['discount_percentage']
            max_discount_amount = request.POST['max_discount_amount']
            valid_from = request.POST['valid_from']
            valid_to = request.POST['valid_to']
            quantity = request.POST['quantity']
            minimum_order_amount = request.POST['minimum_order_amount']

            coupon = Coupons(
                description=description,
                coupon_code=coupon_code,
                coupon_title=coupon_title,
                discount_amount=discount_amount,
                discount=discount,
                maximum_order_amount_the_discount_percenetage_applicable_for=max_discount_amount,
                valid_from=valid_from,
                valid_to=valid_to,
                quantity=quantity,
                minimum_order_amount=minimum_order_amount,
            )
            coupon.save()
            return redirect('coupen')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Coupen_Management_Edit(request, edit_coupen_id):
    if 'admin' in request.session:
        if request.method == 'POST':
            # Check if the coupon with the given edit_coupen_id exists
            coupon = get_object_or_404(Coupons, id=edit_coupen_id)

            # Update the coupon's fields
            coupon.description = request.POST['description']
            coupon.coupon_code = request.POST['coupon_code']
            coupon.coupon_title = request.POST['coupon_title']
            coupon.discount_amount = request.POST['discount_amount']
            coupon.discount = request.POST['discount_percentage']
            coupon.maximum_order_amount_the_discount_percenetage_applicable_for = request.POST[
                'max_discount_amount']
            coupon.valid_from = request.POST['valid_from']
            coupon.valid_to = request.POST['valid_to']
            coupon.quantity = request.POST['quantity']
            coupon.minimum_order_amount = request.POST['minimum_order_amount']
            coupon.active = True  # You can set the active status here

            # Save the updated coupon
            coupon.save()

            return redirect('coupen')

    # return render(request,'adminpanel\coupenmanagment.html')


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Coupen(request):
    if 'admin' in request.session:
        coupen = Coupons.objects.all()

        per_page = 5  # You can change this to your desired number

        paginator = Paginator(coupen, per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'page': page}

    return render(request, 'adminpanel\coupenmanagment.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Order_Management(request):
    if 'admin' in request.session:

        orders = Order.objects.all()

        per_page = 7  # You can change this to your desired number

        paginator = Paginator(orders, per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'page': page}

    return render(request, 'adminpanel/adminordermanagement.html', context)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Orderdetailsmanagement(request, manageorder_id):
    if 'admin' in request.session:

        status_choices = Order.STATUS

        details = Order.objects.get(order_id=manageorder_id)

        user = request.user
        orders = OrderProduct.objects.filter(order_id=details)

        context = {
            'orders': orders,

            'details': details,

            'status_choices': status_choices,
        }
    return render(request, 'adminpanel/adminorderdetailspage.html', context)


def Updatetheoderstatus(request, order_id):

    if request.method == 'POST':
        status = request.POST['status']
        order = Order.objects.get(id=order_id)

        if status == 'Delivered':
            pay = order.payement
            pay.status = 'Paid'
            pay.is_paid = True
            pay.save()

        if status == 'Returned':
            pay = order.payement
            pay.status = 'Returned'
            pay.save()
            walllet = CustomUser.objects.get(id=order.user.id)
            walllet.wallet = float(walllet.wallet) + order.paid_amount
            walllet.save()

        order.status = status
        order.save()

        return redirect('orderdetailsmanagement', order.order_id)


@staff_member_required(login_url='adminlogin')
@cache_control(no_store=True, no_cache=True)
def Productvarientdetails(request, id):
    Productdetails = ProductVariant.objects.get(id=id)

    images = Multipleimges.objects.filter(product=Productdetails)
    context = {'images': images, 'Productdetails': Productdetails}
    return render(request, 'adminpanel\productvarientdetailspage.html', context)


def Admin_Sales_Report(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        orders = Order.objects.filter(created__range=(start_date, end_date))
        total_amount = orders.aggregate(Sum('total'))['total__sum'] or 0

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        header_data = [
            ['NTK OnlineStore Sales Report'],
            [f'Sales Report from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}']
        ]
        header_table = Table(header_data, colWidths=[500])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
        ]))
        elements.append(header_table)

        table_data = []
        table_data.append(
            ['Order ID', 'User', 'Total Amount', 'Status', 'Created Date'])

        for order in orders:
            table_data.append([order.order_id, order.user.first_name + order.user.lastname,
                              f'₹{order.total:.2f}', order.status, str(order.created)])

        order_table = Table(table_data, colWidths=[100, 120, 80, 100, 200])
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(order_table)

        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        return response

    return render(request, 'sales_report_page.html')


def Banner_Management(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        image = request.FILES.get('image', None)
        link_for_pic = request.POST.get('link_for_pic')
        url_for_data = request.POST.get('url_for_data', None)

        if image or link_for_pic and title and url_for_data:

            banner = Banner(title=title, image=image,
                            link=link_for_pic, linkfordata=url_for_data)
            banner.save()

            return redirect('bannermanagement')
    Banner_Details = Banner.objects.all()

    per_page = 2  # You can change this to your desired number

    paginator = Paginator(Banner_Details, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}

    context = {'Banner_Details': Banner_Details, 'page': page}

    return render(request, 'adminpanel/bannermanagement.html', context)


def Delete_banner(request, delete_id):

    delete_item = Banner.objects.get(id=delete_id)
    delete_item.delete()
    return redirect('bannermanagement')


def Edit_banner(request, edit_id):

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image', None)
        link_for_pic = request.POST.get('link_for_pic')
        url_for_data = request.POST.get('url_for_data', None)

        edit_banner = Banner.objects.get(id=edit_id)

        edit_banner.title = title
        edit_banner.image = image
        edit_banner.link = link_for_pic
        edit_banner.linkfordata = url_for_data
        edit_banner.save()
        return redirect('bannermanagement')
