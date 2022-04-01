from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'website/home.html')

def cart(request):
    return render(request, 'website/cart.html')

def viewBook(request):
    return render(request, 'website/viewBook.html')