"""Clothselling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('',views.User_login,name='user_login'),
    path('signup/',views.User_signup,name='user_signup'),
    path('forgetpas/',views.User_forgetpassword,name='forget_password'),
    path('otpverifiaction/<int:user_id>',views.User_otpverification,name='otp_verification'),
    path('resetpas/<int:user_id>',views.User_resetpassword,name='reset_password'),
]
