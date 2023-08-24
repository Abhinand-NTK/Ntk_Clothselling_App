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
from django.urls import path
from .import views



urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('logout/',views.adminlogin,name='logout'),
    path('dashboard/',views.admindashboard,name='admindashboard'),
    path('users/',views.adminusers,name='adminusers'),
    path('products/',views.adminproducts,name='adminproducts'),
    path('category/',views.admincategory,name='category'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('editcategory/<str:id>',views.editcategory,name='editcategory'),
    path('addsubcategory/',views.addsubcategory,name='addsubcategory'), 
    path('editsubcategory/<str:id>',views.editsubcategory,name='editcategory'),
    path('addcolorsize/',views.addcolor_size,name='addcolorsize'),  
    path('editcolorsize/<str:id>',views.edit_color_size,name='editcolorsize'),  
    path('addproducts',views.adminaddproducts,name='addproducts'),  
    path('editproducts/<str:id>',views.admineditproducts,name='editproducts'),  
    path('productvarients/', views.adminproductsvarients, name='productvarients'),
    path('editproductvarients/<str:id>', views.admineditproductsvarients, name='productvarients'),
]
   


