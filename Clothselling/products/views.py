from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from admin_auth.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core import serializers

# Create your views here.

def home(request):

    products=Product.objects.all().order_by('-id')[:8]
    productsvarient=ProductVariant.objects.all()
    brand=Brand.objects.all()
    banner=Banner.objects.all()

    mens=Product.objects.filter(men=True)
    count1 = mens.count()  # Get the count of items in the queryset
    request.session.save()

    Womans=Product.objects.filter(woman=True)
    count2 = Womans.count()  # Get the count of items in the queryset
    request.session.save()

    kids=Product.objects.filter(kids=True)
    count3 = kids.count()  # Get the count of items in the queryset
    request.session.save()

    combos=Product.objects.filter(combos=True)
    count4 = combos.count()  # Get the count of items in the queryset
    request.session.save()


    context={'count1':count1,'count2':count2,'count3':count3,'count4':count4,'products':products,
            'brand':brand,'banner':banner}

    return render(request,"home.html",context)

def product_category(request):

    sizes=Size.objects.all()
    color=Color.objects.all()
  

    context={'sizes':sizes,'color':color}

    return render(request,'category_management_userside.html',context)

from django.core.paginator import Paginator

def Womans(request,id=None):

    items_per_page = 6

    if id:
        id_sub=Subcategory.objects.get(name=id)
        products=Product.objects.filter(woman=True,men=False,combos=False,kids=False,subcategory=id_sub)
        min_prices_per_product = []

        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = []  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.append(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes  
    elif id==None:
        products = Product.objects.filter(woman=True, men=False, combos=False, kids=False)

        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = set()  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.add(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes  # Assign the list of sizes to the product in the sizes dictionary
        
    elif request.method == 'POST':
        pass

    products_for_filter=Product.objects.filter(woman=True,men=False,combos=False,kids=False)
    heading="Woman"
    cat = set()
    for product in products_for_filter:
        subcategory = product.subcategory  # Assuming 'subcategory' is a field in your Product model
        cat.add(subcategory)

        
    per_page = 6  # You can change this to your desired number

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    zipped_data = zip(page, min_prices_per_product)



    size=Size.objects.all()
    color=Color.objects.all()

   

    context={'page':page,'products':products,'cat':cat,'heading':heading,'min_prices_per_product':min_prices_per_product,'zipped_data':zipped_data,'sizes':sizes,'size':size,'color':color,}



    

    return render(request,"category_management_userside.html",context)

def Mens(request,id=None):

    if id:
   

        id_sub=Subcategory.objects.get(name=id)
        
        products=Product.objects.filter(woman=False,men=True,combos=False,kids=False,subcategory=id_sub)
        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = []  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.append(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 
    else:

        products=Product.objects.filter(woman=False,men=True,combos=False,kids=False)
        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = set()  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.add(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 
    
    products_for_filter=Product.objects.filter(woman=False,men=True,combos=False,kids=False)


    heading="Men"
  
    cat = set()
    for product in products_for_filter  :
        subcategory = product.subcategory  # Assuming 'subcategory' is a field in your Product model
        cat.add(subcategory)

    per_page = 6  # You can change this to your desired number

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    zipped_data = zip(page, min_prices_per_product)


    size=Size.objects.all()
    color=Color.objects.all()

    context={'page':page,'products':products,'cat':cat,'heading':heading,'min_prices_per_product':min_prices_per_product,'zipped_data':zipped_data,'sizes':sizes,'size':size,'color':color}
    return render(request,"category_management_userside.html",context)

def kids(request,id=None):
    if id:
        id_sub=Subcategory.objects.get(name=id)

        products=Product.objects.filter(woman=False,men=False,combos=False,kids=True,subcategory=id_sub)

        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = []  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.append(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 
    else:
        products=Product.objects.filter(woman=False,men=False,combos=False,kids=True)
        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = set()  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.add(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 


    products_filter=Product.objects.filter(woman=False,men=False,combos=False,kids=True)

    heading="Kids"
    cat = set()
    for product in products_filter:
        subcategory = product.subcategory  # Assuming 'subcategory' is a field in your Product model
        cat.add(subcategory)


    per_page = 6  # You can change this to your desired number

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    zipped_data = zip(page, min_prices_per_product)

    
    size=Size.objects.all()
    color=Color.objects.all()

    context={'page':page,'products':products,'cat':cat,'heading':heading,'min_prices_per_product':min_prices_per_product,'zipped_data':zipped_data,'sizes':sizes,'size':size,'color':color}
    return render(request,"category_management_userside.html",context)

def combos(request,id=None):

    if id:
        id_sub=Subcategory.objects.get(name=id)

        products=Product.objects.filter(woman=False,men=False,combos=True,kids=False,subcategory=id_sub)

        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = set()  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.add(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 
    else:
        products=Product.objects.filter(woman=False,men=False,combos=True,kids=False)

        min_prices_per_product = []
        sizes = {}

        for product in products:
            product_variants = ProductVariant.objects.filter(product=product)

            min_price = None
            product_sizes = set()  # Create a list to store sizes for the current product

            for variant in product_variants:
                price = variant.price
                size = variant.size

                if min_price is None or price < min_price:
                    min_price = price

                product_sizes.add(size)  # Add size to the product_sizes list

            min_prices_per_product.append(min_price)
            sizes[product.name] = product_sizes 



    products_filter=Product.objects.filter(woman=False,men=False,combos=True,kids=False)
    heading="Combos"
    cat = set()
    for product in products_filter:
        subcategory = product.subcategory  # Assuming 'subcategory' is a field in your Product model
        cat.add(subcategory)

    
    per_page = 6  # You can change this to your desired number

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    zipped_data = zip(page, min_prices_per_product)
    
    size=Size.objects.all()
    color=Color.objects.all()
    

    context={'page':page,'size':size,'color':color,'products':products,'cat':cat,'heading':heading,'min_prices_per_product':min_prices_per_product,'zipped_data':zipped_data,'sizes':sizes}
    return render(request,"category_management_userside.html",context)

def product_details(request,id):

    product = get_object_or_404(Product, id=id)
    product_variants = ProductVariant.objects.filter(product=product)
    serialized_product_variants = serializers.serialize('json', product_variants)
    request.session['product_variants_json'] = serialized_product_variants

    product_variant_images = {}

    for variant in product_variants:
        variant_images = Multipleimges.objects.filter(product=variant)
        first_image = variant_images.first()
        
        if first_image:
            # Store the URL of the first image and variant color in the dictionary
            product_variant_images[variant.id] = (first_image.images.url, variant.color)





    product_vareint_data=[]
    for varient in product_variants:
        varient_data={
            'color' : varient.color,
            'price' : varient.price,
            'size' : varient.size,
        }
        product_vareint_data.append(varient_data)

    for varient_data in product_vareint_data:
        print(varient_data['color'])


    color=Color.objects.get(name='Black')


    product_variants1=ProductVariant.objects.filter(product=product,color=color)
    
    images = Multipleimges.objects.filter(product__in=product_variants)
    testing = Multipleimges.objects.filter(product__in=product_variants1)


    size=Size.objects.all()
    color=Color.objects.all()

    context = {'size':size,'color':color,'product': product, 'product_variants': product_variants, 'images': images,'product_vareint_data':product_vareint_data,'product_variant_images': product_variant_images}
   
    return render(request,'products_detalils.html',context)

import json
def Filtering_in_Prouduct_details_page(request):


   

    if request.method=='POST':

        data = json.loads(request.body.decode('utf-8'))

            # Access the values sent from the frontend
            
        color = data.get('color')
        variant_id = data.get('variant_id')
      
            
        varient=ProductVariant.objects.get(id=variant_id)

        varient_color = str(varient.color) 
        varient_size = str(varient.size) 
        varient_price = str(varient.price) 
        varient_stock = str(varient.stock) 
        varient_id = str(variant_id) 
         

        testing = Multipleimges.objects.filter(product=varient)
        

        image_urls = [img.images.url for img in testing]

        response = {'varient_id': varient_id,'varient_stock': varient_stock,'varient_price': varient_price,'varient_size': varient_size,'varient_color': varient_color, 'image_urls': image_urls}
        
        return JsonResponse(response)  # This line sends a JSON response with the 'varient_color' key


    
def Filter(requset,category_id=None,heading=None):


    current_route = requset.path

    segments = current_route.strip('/').split('/')
    last_segment = segments[-1] if segments else None

    if last_segment == 'Men':
        return Mens(requset,category_id)
    elif last_segment == 'Woman':
        return Womans(requset,category_id)
    elif last_segment == 'Kids':
        return kids(requset,category_id)
    elif last_segment == 'Combos':
        return combos(requset,category_id)
    
def filter_Accordence_multiple_input(request,heading=None):
    current_route = request.path

    segments = current_route.strip('/').split('/')

    last_segment = segments[-1] if segments else None

    if request.method == 'POST':

        selected_colors = request.POST.getlist('colorCheckbox')
        selected_sizes = request.POST.getlist('sizeCheckbox')

        # selected_brand = request.POST.getlist('brandCheckbox')

        min_range_value = request.POST.get('myRangeMin', None)
        max_range_value = request.POST.get('myRangeMax', None)


        # name=request.POST['name_search']
        name=request.POST.get('name_search',None)



        if  min_range_value == 0 :
            min_range_value = None

        # Check if max_range_value is empty or not provided
        if  max_range_value == 0 :
            max_range_value = None



        if last_segment == 'Men':

            products_in=Product.objects.filter(woman=False,men=True,combos=False,kids=False)
            heading="Men"


        if last_segment == 'Woman':

            products_in=Product.objects.filter(woman=True,men=False,combos=False,kids=False)
            heading="Woman"


        if last_segment == 'Kids':

            products_in=Product.objects.filter(woman=False,men=False,combos=False,kids=True)
            heading="Kids"


        if last_segment == 'Combos':

            products_in=Product.objects.filter(woman=False,men=False,combos=True,kids=False)
            heading="Combos"



        products = ProductVariant.objects.filter(product__in=products_in)

        if min_range_value is not None and max_range_value is not None:

            products = products.filter( Q(price__gte=min_range_value) & Q(price__lte=max_range_value))

        if selected_colors:
            products = products.filter(color__in=selected_colors)
        
        if selected_sizes:
            products = products.filter(size__in=selected_sizes)
        
        if name:


            if heading ==  "Men":

                product = Product.objects.filter(name__icontains=name,men=True,woman=False,kids=False,combos=False)

                products = ProductVariant.objects.filter(product__in=product)

            if heading ==  "Woman":

                product = Product.objects.filter(name__icontains=name,men=False,woman=True,kids=False,combos=False)

                products = ProductVariant.objects.filter(product__in=product)
            
            if heading ==  "Kids":

                product = Product.objects.filter(name__icontains=name,men=False,woman=False,kids=True,combos=False)
            
            if heading ==  "Combos":

                product = Product.objects.filter(name__icontains=name,men=False,woman=False,kids=False,combos=True)


                products = ProductVariant.objects.filter(product__in=product)


        

        product_data=set()

        product_data = (
            {
                'id':product.product.id,
                'name': product.product.name,
                'color': product.color.name,
                'size': product.size.name,
                'price': product.price,
                'image':product.product.images.url
                # Add more fields as needed
            }
            for product in products
        )


        size=Size.objects.all()
        color=Color.objects.all()

        response_data = {
            'message': 'Success',
            'products': product_data,
            'size':size,
            'color':color,
            'heading':heading,
        }


       

        # Send a JSON response back to the JavaScript code
        # return JsonResponse(response_data)
        return render(request,'multiplefilterproducts.html',response_data)
 

from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def search_products(request,query):

    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    # query = request.GET.get('query', '').strip()
    query1=query

    if query:
        # Query your database to find matching products
        products = Product.objects.filter(name__icontains=query1)[:10]  # Adjust the query as needed

        # Return product names as JSON
        suggestions = [{'name': product.name} for product in products]
    else:
        suggestions = []  # No query, return an empty list

    return JsonResponse(suggestions, safe=False)





    

    



    
    






