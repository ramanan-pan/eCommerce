from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'website/home.html')

def create(request):
    return render(request, 'website/create.html')

def createsuccess(request):
    return render(request, 'website/createsuccess.html')

def editaccount(request):
    return render(request, 'website/editaccount.html')

def forgotpassword(request):
    return render(request, 'website/forgotpassword.html')

def login(request):
    return render(request, 'website/login.html')

def recoversent(request):
    return render(request, 'website/recoversent.html')

