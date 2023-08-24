from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from admin_auth.models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings
from random import randint

# Create your views here.


def User_login(request):

    if request.method=='POST':
        password=request.POST['password']
        email=request.POST['username']
        print(password)
        print(email)

        hashed_password = make_password(password, hasher='pbkdf2_sha256')

        # Authenticate the user
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            return redirect('home')
        else:
            return redirect('user_login')
        


    return render(request,'Authenticatoins/loginpage.html')


def User_signup(request):

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        check=CustomUser.objects.filter(email=email)
        # check=CustomUser.objects.filter(phonenumber=username)

        
        if check:
            messages.error(request,'The E-mail is Already exist Try with another one')
            return redirect('user_signup')

           
        else:
            
            
            otp = generate_and_send_otp()  # Generate OTP here
            user=CustomUser.objects.create_user(email,password=password)
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
