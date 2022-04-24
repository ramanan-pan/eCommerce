"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from website.admin import vendorSite, clientSite
from django.urls import path
from . import views

app_name = "website"

urlpatterns = [

    path('', views.home, name='website-home'),
    #path('ordersummary/', views.ordersum, name='Order-summary'),
    path('orderconfirmation', views.conf, name='Order-confirmation'),
    path('ordersummary', views.ordersum, name="website-orderSummary"),
    path('reservesummary', views.reservesum, name='website-reserveSummary'),
    path('reserveconfirmation', views.reserveconf, name='website-reserve-confirmation'),
    path('create', views.create, name='website-create'),
    path('createsuccess', views.createsuccess, name='website-createsuccess'),
    path('editaccount', views.editaccount, name='website-editaccount'),
    path('forgotpassword', views.forgotpassword, name='website-forgotpassword'),
    path('login', views.login, name='website-login'),
    path('welcome', views.welcome, name='website-welcome'),
    path('index', views.index, name='website-index'),
    path('clientview', views.cv, name='website-clientview'),
    path('recoversent', views.recoversent, name='website-recoversent'),
    path('cart/', views.cart, name='website-cart'),
    path('viewBook/', views.viewBook, name='website-viewBook'),
    path('manageusers/', views.mangusers, name = 'website-site1-manageusers'),
    path('viewBook/', views.viewBook, name='website-viewBook'),
    path('cart/add/', views.cart_add, name='website-cart_add'),
    path('cart/delete/', views.cart_delete, name='website-cart_delete'),
    path('cart/update/', views.cart_update, name='website-cart_update'),
    path('book/<slug:slug>', views.book_detail, name='website-book_detail'),
    path('editbook/<slug:slug>', views.book_edit, name='website-book_edit'),
    path('validateCreds', views.validateCreds, name='website-validate'),
    path('addUser', views.addUser, name='website-addUser'),
    path('changeAccount', views.changeAccount, name='website-changeAccount'),
    path('home/', views.home, name='website-home'),
    path('adset/', views.adset, name='website-adset'),
    path('cliset/', views.cliset, name='website-adset'),
    path('venset/', views.venset, name='website-adset'),
    path('changePassword', views.changePassword, name='website-changePassword'),
    path('deleteAccount', views.deleteAccount, name='website-deleteAccount'),
    path('inventory', views.inventory, name='website-inventory'),
    path('manageusers', views.mangusers, name='website-adminmanage-users'),
    path('managevendors', views.mangvend, name='website-adminmanage-vendors'),
    path('managepromotions', views.mangprom, name='website-adminmanage-promotions'),
    path('manageorders', views.mangord, name='website-adminmanage-orders'),
    path('adminview', views.adminmain, name='website-adminview'),
    path('vendorsettings', views.vendorset, name='website-vendorsettings'),
    path('vendorview', views.vendview, name='website-vendorview'),
    path('passwordRecovery', views.passwordRecovery, name='website-passwordRecovery'),
    path('logout', views.logout, name='website-logout'),
    path('testimage', views.image, name='website-test-image'),
    path('reserve', views.res, name='website-reservationsmanagement'), 
    path('expiredpu', views.expiry, name='website-reservationsmanagement')
]
