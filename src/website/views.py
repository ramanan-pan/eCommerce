from django.shortcuts import render

from .models import Book

# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'website/index.html', {'books': books})
    
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

def addUser(request):
    if request.POST != None:
        print('OH') #data base stuff happens here makes a new user
    else:
         return render(request, 'website/create.html') #required fields not filled in return to sign up

    return render(request, 'websit/create.html')

def createsuccess(request):
    return render(request, 'website/createsuccess.html')

def editaccount(request):
    return render(request, 'website/editaccount.html')

def changeAccount(request):

    if request.POST != None:
        print('OH') # datebase stuff happens here changes user account values
    else:
        print('NO') # Nothing happens 

    return render(request, 'website/editaccount.html')

def forgotpassword(request):
    return render(request, 'website/forgotpassword.html')

def login(request):
    return render(request, 'website/login.html')

def validateCreds(request):
    if request.POST != None:
        if request.POST['username'] == 'User' and request.POST['password'] == 'Pass': #test case
            return render(request, 'website/welcome.html') #take to the welcome screen if user + pass combo is found
        else:
            return render(request, 'website/login.html') #reroute to login if user and password does not match
    else:
        return render(request, 'website/welcome.html') #no form data return to login


def recoversent(request):
    return render(request, 'website/recoversent.html')

def cart(request):
    return render(request, 'website/cart.html')

def viewBook(request):
    return render(request, 'website/viewBook.html')
