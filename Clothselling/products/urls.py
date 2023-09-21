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

urlpatterns=[
    path('',views.home,name='home'),
    path('category_selection/',views.product_category,name='category_selection'),
    path('womans/',views.Womans,name='womans'),
    path('mens/',views.Mens,name='mens'),
    path('kids/',views.kids,name='kids'),
    path('combos/',views.combos,name='combos'),
    path('products_details/<int:id>',views.product_details,name='details'),
      ]

