from django.shortcuts import render,redirect,HttpResponse
from admin_auth.models import *
from user_auth.models import *
from .models import Cart
from products import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone


# Create your views here.

def Cart_page(request):

    user = request.session['user']
    user_id = CustomUser.objects.get(email=user)

    if 'user' in request.session:
        cart = Cart.objects.filter(user=user_id)
        total_price = 0  # Initialize total price

        for cart_item in cart:
            cart_item.total_price = cart_item.quantity * cart_item.products.price
            total_price += cart_item.total_price
        
        context = {'cart': cart, 'total_price': total_price}
        return render(request, 'cart_page.html', context)

    # Handle the case where user is not logged in
    return render(request, 'cart_page.html')


def Add_to_Cart(request, product_vareint_id):

    if 'user' in request.session:
        user = request.session['user']
        user_id = CustomUser.objects.get(email=user)

        if request.method == 'POST':
            quantity = int(request.POST['quantity'])
            product_variant = ProductVariant.objects.get(id=product_vareint_id)

            cart_item, created = Cart.objects.get_or_create(
                user=user_id,
                products=product_variant,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return redirect('cart_item')

    return redirect('cart_item')

def Cart_delete(request,delete_id):
    if 'user' in request.session:
       delete = Cart.objects.get(id=delete_id)
       
       delete.delete()
       return redirect('cart_item')
    
    
def Checkout(request):

    # if 'show_modal' in request.session:
    #     del request.session['show_modal']
    #     request.session.save()


    if 'user' in request.session:
        
        user = request.session['user']
        user_id = CustomUser.objects.get(email=user)
    
        cart = Cart.objects.filter(user=user_id)
        total_price = 0  # Initialize total price
        discount_price = 0  # Initialize discount price
        tax = 0 #for intial tax
        GrandTotal=0

        for cart_item in cart:
            cart_item.total_price = cart_item.quantity * cart_item.products.price
            total_price += cart_item.total_price

        request.session['redirected'] = False

  
        if request.method == 'POST':
            coupencode = request.POST.get('coupencode')  # Use get to avoid raising an error if 'coupencode' is not present
            

            request.session['coupencode'] = coupencode 

            # coupon = Coupons.objects.filter(coupon_code=coupencode).first()

            current_datetime = timezone.now()

            try:
                coupon = Coupons.objects.get(coupon_code=coupencode, valid_from__lte=current_datetime, valid_to__gte=current_datetime)
            except Coupons.DoesNotExist:
                coupon = None  # Set coupon to None when it doesn't exist
                messages.error(request, "The coupon does not exist or is not valid")
                return redirect('check_out')
        

            if coupon and coupon.active:
                if coupon.discount_amount > 0 and total_price >= coupon.minimum_order_amount:
                    discount_price = coupon.discount_amount
                    messages.success(request,'Applied Sucessfully')
                    # return redirect('check_out')
                elif coupon.discount > 0 and total_price >= coupon.minimum_order_amount:
                    if total_price < coupon.maximum_order_amount_the_discount_percenetage_applicable_for:
                        discount_price = (total_price * coupon.discount) / 100
                    else:
                        discount_price = (coupon.maximum_order_amount_the_discount_percenetage_applicable_for * coupon.	discount) / 100
                else:
                    messages.error(request, f"Applicable only for :- {coupon.minimum_order_amount}")

               
            else:
                messages.error(request,"The coupen  is not valid")
        if total_price>0 and total_price<1000:
            tax=(total_price*5)/100
        elif total_price >0 and total_price >1000:
            tax=(total_price*12)/100
        GrandTotal=total_price-discount_price+tax
        address_user = UserAdress.objects.filter(user=user_id)

        if GrandTotal <= 0:
            if not request.session.get('redirected', False):  # Check if not already redirected
                request.session['redirected'] = True  # Set the flag
                messages.error(request, "There is nothing in the cart to proceed!!!!!")
                return redirect('cart_item')
        else:
            pass
        #Continue with the rest of your checkout logic

        coupen=Coupons.objects.all()

        context = {
            'address_user': address_user,
            'total_price': total_price,
            'cart': cart,
            'discount_price': discount_price,
            'tax':tax,
            'GrandTotal':GrandTotal,
            'coupen':coupen
        }
        return render(request, 'checkout.html', context)
    else:
        # Handle the case when 'user' is not in the session
        # Redirect to login or show an error message, for example
        return redirect('login')  # Replace 'login' with the appropriate URL or view name



def update_cart_item_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        action = request.POST.get('action')
        cart_item = Cart.objects.get(id=item_id)

        if action == 'incr':
            cart_item.quantity += 1
        elif action == 'decr' and cart_item.quantity > 0:
            cart_item.quantity -= 1

        cart_item.save()
        
        total_price = cart_item.products.price * cart_item.quantity

        response_data = {'new_quantity': cart_item.quantity, 'new_total_price': total_price}
        return JsonResponse(response_data)


    




            
    

                