from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from admin_auth.models import CustomUser
from user_auth.models import UserAdress
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from random import randint

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
            # else: 
            #     # request.session.flush
            #     print("Its coming here !!!")
            #     messages.error(request,"Your Acccount is blocked")
            #     User_logout()
            #     # return redirect('user_login')
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

def Myprofile(request):
    if 'user' in request.session:
        
        personal_details = CustomUser.objects.all()
        context = {'personal_details': personal_details}
        
    return render(request, 'myprofile.html', context)
   
    
def Manage_Address(request):
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


            # if not firstname or not lastname:
            #     firstname=user.first_name
            #     lastname=user.lastname
            # else:
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
            return redirect('manageadress')
    address_user=UserAdress.objects.filter(user=user)
    context={
        'address_user':address_user
    }

  
    return render(request,'manageadress.html',context)  

def Manage_Edit_Address(request,adress_id):
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


            # if not firstname or not lastname:
            #     firstname=user.first_name
            #     lastname=user.lastname
            # else:
            address=UserAdress.objects.get(id=adress_id)
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
            return redirect('manageadress')
    address_user=UserAdress.objects.filter(user=user)
    context={
        'address_user':address_user
    }

  
    return render(request,'manageadress.html',context)  

def Manage_Address_delete(request,adress_id):
    if 'user' in request.session:
        user=request.user
        
    
    else:
        messages.error(request,'Session time Out')
        return redirect('user_login')
    address=UserAdress.objects.get(id=adress_id)
    address.delete()
    return redirect('manageadress')

def Edit_profile(request):
    if "user" in request.session:
         print("Hello world!!!")
         if request.method == 'POST':
            # return HttpResponse(True)
            print('Abhinand is a brillent Man  !!!!!!!!!!!!!!!!!!!!')
            firstname = request.POST['first_name']
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

        
    else:
        print("Hello world!!!")
        return HttpResponse(False)
        messages.error(request,'Sesson time Out')
        return redirect('user_login')
        

   
        