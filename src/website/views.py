from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'website/index.html')
    
def welcome(request):
    return render(request, 'website/welcome.html')

def cv(request):
    return render(request, 'website/ClientView.html')

def home(request):
    return render(request, 'website/home.html')

def conf(request):
    return render(request, 'website/orderconf.html')

def adset(request):
    return render(request, 'website/addex.html') 

def ordersum(request):
    return render(request, 'website/ordersummary.html')

def adminmain(request):
    return render(request, 'website/adminmain.html')

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

def cart(request):
    return render(request, 'website/cart.html')

def viewBook(request):
    return render(request, 'website/viewBook.html')

def mangusers(request):
    return render(request, 'website/manageusers.html')