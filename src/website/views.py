from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'website/home.html')

def conf(request):
    return render(request, 'website/orderconf.html')

def adset(request):
    return render(request, 'website/index.html') 

def ordersum(request):
    return render(request, 'website/ordersummary.html')

def adminmain(request):
    return render(request, 'website/adminmain.html')