from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from admin_auth.models import CustomUser
from user_auth.models import UserAdress
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from random import randint
from order.models import *
from collections import defaultdict

# Create your views here.


def User_login(request):
    if 'admin' in  request.session:
            return redirect('admindashboard')

    if request.method=='POST':
        password=request.POST['password']
        email=request.POST['username']

        
     
        hashed_password = make_password(password, hasher='pbkdf2_sha256')

        # Authenticate the user
        user = authenticate(email=email, password=password)
        check=CustomUser.objects.filter(email=email)
        # is_verify=user.is_verified
      


        if user:
                if  user.is_blocked:
                    print("Its coming here !!!")
                    messages.error(request,"Your Acccount is blocked")
                    User_logout(request)

                elif user.is_verified and user.is_authenticated and not user.is_blocked:
                    userlogin(request, user)  # Log the user in
                    request.session['user'] = email
                    # if user in request.session:
                    
                    return redirect('home')
                else:
                    return redirect('otp_verification', user_id=user.id)
          
        else:
            messages.error(request, "Check the email or password")
            # return redirect('user_login')


    return render(request,'Authenticatoins/loginpage.html')

def userlogin(request,user):
    login(request,user)


def User_logout(request):
    logout(request)
    if 'user' in request.session:
        del request.session['user']
    return redirect('user_login')
    


def User_signup(request):

    if request.method=='POST':
        email=request.POST['username']
        password=request.POST['password']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        # phonenumber=request.POST['phonenumber']
        repeatpassword=request.POST['repeatpassword']

        check=CustomUser.objects.filter(email=email)


        
        if check:
            messages.error(request,'The E-mail is Already exist Try with another one')
            return redirect('user_signup')
        if password==repeatpassword:
         
            
            otp = generate_and_send_otp()  # Generate OTP here
            user=CustomUser.objects.create_user(email,password=password,)
            user.first_name = firstname
            user.lastname = lastname
            # user.phone_number = phonenumber
            user.otp=otp
            user.save()
            user_id=user.id
            

            send_mail(
                "Please use this otp for the further process",
                f"your otp for signup is :{otp}",
                "testntk123@gmail.com",
                [email,],
                fail_silently=False,
            )
            return redirect('otp_verification',user_id)
        else:
            messages.error(request,'Password fiels are Not matchining  !')
            return redirect('user_signup')

    return render(request, 'Authenticatoins/signup.html')


def generate_and_send_otp():
    otp = randint(100000, 999999)
    print(otp)
    return otp

def User_otpverification(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {'user': user}
    print(user.otp)

    if request.method == 'POST':
        verification = request.POST['otp']
        print(verification)

        if verification==user.otp:
            user.otp = ''
            user.is_verified = True
            user.save()  # Save the user after updating is_email_verified
            messages.success(request, 'Email verification is successful')
            return redirect('user_login')  # Use return to perform the redirect
        else:
            messages.error(request, 'Please enter a valid OTP')

    return render(request, 'Authenticatoins/verification.html', context)


def User_forgetpassword(request):
    if request.method == 'POST':
        reset_email = request.POST['resetpassword']
        try:
            user = CustomUser.objects.get(email=reset_email)
            return redirect('reset_password', user_id=user.id)
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
    return render(request, 'Authenticatoins/forgotpassword.html')

def User_resetpassword(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('user_login')
    
    if request.method == 'POST':
        password = request.POST['resetpassword']
        repeat_password = request.POST['password']
        if password == repeat_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('user_login')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'Authenticatoins/resetpassword.html', {'user': user})

    
def Manage_Address(request):
    current_path = request.path
    if 'user' in request.session:
        user=request.user
    
    else:
        messages.error(request,'Sesson time Out')
        return redirect('user_login')
        
    if request.method=='POST':
            print("Abhinand")
            
            first_name=request.POST['firstname']
            last_name=request.POST['lastname']
            phonenumber=request.POST['phonenumber']
            address=request.POST['address']
            town=request.POST['town']
            zip_code=request.POST['zipcode']
            nearbylocation=request.POST['nearbylocation']
            district=request.POST['district']

            address=UserAdress(
                user=user,
                first_name=first_name,
                last_name=last_name,
                phonenumber=phonenumber,
                address=address,
                town=town,
                zip_code=zip_code,
                nearbylocation=nearbylocation,
                district=district
                )
            address.save()

            if '/cart/check_out' in request.META['HTTP_REFERER']:
                 return redirect('check_out')
            elif '/manageadress' in request.META['HTTP_REFERER']:
                return redirect('manageadress')
    address_user=UserAdress.objects.filter(user=user)
    context={
        'address_user':address_user
    }

  
    return render(request,'manageadress.html',context)  

def Manage_Edit_Address(request, adress_id):
    if 'user' in request.session:
        user = request.user
    else:
        messages.error(request, 'Session time Out')
        return redirect('user_login')
        
    try:
        address = UserAdress.objects.get(id=adress_id, user=user)
    except UserAdress.DoesNotExist:
        messages.error(request, 'Address not found')
        return redirect('manageadress')
    
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phonenumber = request.POST['phonenumber']
        address_text = request.POST['address']
        town = request.POST['town']
        zip_code = request.POST['zipcode']
        nearby_location = request.POST['nearbylocation']
        district = request.POST['district']

        # Update the address fields
        address.first_name = first_name
        address.last_name = last_name
        address.phonenumber = phonenumber
        address.address = address_text
        address.town = town
        address.zip_code = zip_code
        address.nearbylocation = nearby_location
        address.district = district

        # Save the changes
        address.save()
        if '/cart/check_out' in request.META['HTTP_REFERER']:
                 return redirect('check_out')
        elif '/manageadress' in request.META['HTTP_REFERER']:
                return redirect('manageadress')

        # return redirect('manageadress')

    context = {
        'address_user': [address],  # Pass the address as a list to the template
    }

    return render(request, 'manageadress.html', context)

def Manage_Address_delete(request,adress_id):
    if 'user' in request.session:
        user=request.user
        
    
    else:
        messages.error(request,'Session time Out')
        return redirect('user_login')
    address=UserAdress.objects.get(id=adress_id)
    address.delete()
    if '/cart/check_out' in request.META['HTTP_REFERER']:
                 return redirect('check_out')
    elif '/manageadress' in request.META['HTTP_REFERER']:
                return redirect('manageadress')


def Myprofile(request):
    if 'user' in request.session:
        if request.method=='POST':
            return render(request, 'manageadress.html')

        
    personal_details = CustomUser.objects.all()
    context = {'personal_details': personal_details}
        
    return render(request, 'myprofile.html', context)
    


    
def Edit_profile(request):
    # if 'user' in request.session:
         print("Hello world!!!")
         if request.method == 'POST':
            # return HttpResponse(True)
            print('Abhinand is a brillent Man  !!!!!!!!!!!!!!!!!!!!')
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            user_email = request.user  # Access the email using request.user.email
            user = CustomUser.objects.get(email=user_email)  # Get the user by email
            
            if user.check_password(password):  # Use check_password to verify the password
                user.first_name = firstname
                user.lastname = lastname  # Correct the attribute name to last_name
                user.save()  # Call the save method to save changes
                
                messages.success(request, "Profile updated successfully")
                return redirect('myprofile')
            else:
                messages.error(request, "Incorrect password")
                return redirect('myprofile')
            
         return render(request,'myprofile.html')
    # else:
    #     return redirect('myprofile')


def Myorder(request):

    # if 'show_modal' in request.session:
    #     del request.session['show_modal']
        
    user = request.user
    orders = OrderProduct.objects.filter(customer=user)
    # return HttpResponse(orders)
    
    order_dict = defaultdict(list)

    for order in orders:
        order_dict[order.order_id].append(order)

    context = {
        'order': orders,
        'order_dict': dict(order_dict),  # Convert defaultdict to a regular dictionary
    }

    return render(request, 'myorder.html', context)
def Coupenlist(requset):
    coupens=Coupons.objects.all()
    context={
         'coupens':coupens
         }
    return render(requset,'coupenlistuserside.html',context)

def Mywallet(request):
     return render(request,'mywallet.html')

def Mywishlist(request, varient_id):
    color = ''  # Initialize color variable

    if varient_id: 
        product_variant_instance = get_object_or_404(ProductVariant, id=varient_id)

        try:
            wishlist_exist_or_not = Wishlist.objects.get(product=product_variant_instance)
            wishlist_exist_or_not.check_color=False
            wishlist_exist_or_not.delete()
            color = 'red'  # Set color to 'red' when an item is removed
            return JsonResponse({'message': 'The item is removed from the Wishlist'})
        except Wishlist.DoesNotExist:
            wishlist = Wishlist(product=product_variant_instance)
            wishlist_exist_or_not.check_color=True
            wishlist.save()
            color = 'black'  # Set color to 'black' when an item is added
            return JsonResponse({'message': 'The item is added to the Wishlist'})
        
    return render(request, 'wishlist.html', {'color': color})




    

   
        