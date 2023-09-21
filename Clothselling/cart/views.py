from django.shortcuts import render,redirect
from admin_auth.models import *
from user_auth.models import *
from .models import Cart
from products import *

# Create your views here.

def Cart_page(request):
    if 'user' in request.session:
        cart = Cart.objects.all()
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
                # Update cart item's quantity
                cart_item.quantity += quantity
                cart_item.save()

            # Update product stock
            product_variant.stock -= quantity
            product_variant.save()

            return redirect('cart_item')

    return redirect('cart_item')

def Cart_delete(request,delete_id):
    if 'user' in request.session:
       delete = Cart.objects.get(id=delete_id)
       delete.delete()
       return redirect('cart_item')
def Checkout(request):
    if 'user' in request.session:
        user=request.session['user']
        user_id=CustomUser.objects.get(email=user)
    address=UserAdress.objects.filter(user=user_id)
    context={'address':address}
    return render(request,'checkout.html',context)



            
    

                