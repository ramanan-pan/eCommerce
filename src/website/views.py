<<<<<<< HEAD
from django.shortcuts import render
from django.template import RequestContext
from .models import *

=======
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import redirect, render
import re
from .models import User
>>>>>>> refs/remotes/origin/main
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
    books = Book.objects.all()
    price = books.aggregate(price = Sum('price'))['price']
    discount = 0
    if request.POST.get('DISCOUNT'):
        discount = int(request.POST.get('DISCOUNT'))
    if request.method == "POST":
        sale = Sale()
        sale.purchaser = request.POST.get('CARD') #TODO switch with user ID
        sale.totalPrice = price + discount + 20
        sale.save()
        return render(request, 'website/orderconf.html', {'price' : price, 'books' : books, 'sale' : sale, 'discount' : discount})
    return render(request, 'website/orderconf.html', {'price' : price})

def adset(request):
    return render(request, 'website/addex.html') 

def ordersum(request):
    books = Book.objects.all()
    price = books.aggregate(price = Sum('price'))['price']
    if request.method == "POST" and request.POST.get('CODE'):
        discount = 0
        try:
            promo = Promotion.objects.filter(code=request.POST.get('CODE'))[0]
            if promo.pctdiscount:
                discount = -price*promo.pctdiscount
            else:
                discount = -promo.amountdiscount
        finally:
            return render(request, 'website/ordersummary.html', {'books' : books, 'price' : price, 'discount' : discount})
    #TODO get the list of books from the user session.
    return render(request, 'website/ordersummary.html', {'books' : books, 'price' : price})

def adminmain(request):
    return render(request, 'website/adminmain.html')

def create(request):
    return render(request, 'website/create.html')

def addUser(request):
    regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regexDOB = '^(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\\d\\d$'

    if request.method == 'POST' and request.POST != None:
        if not request.POST['email']: #checks for an empty user input 
            messages.info(request, ' Email Empty') # tells the user what is wrong
            return redirect(create) #returns user back to the creation screen
        if not request.POST['firstName']:
            messages.info(request, ' First Name Empty')
            return redirect(create)
        if not request.POST['lastName']:
            messages.info(request, 'Last Name Empty')
            return redirect(create)
        if not request.POST['address1']:
            messages.info(request, 'Address 1 Empty')
            return redirect(create)
        #if not request.POST['address2']:
        #   messages.info(request, 'Adress 2 Empty')
        #  return redirect(create)
        if not request.POST['zipcode']:
            messages.info(request, 'Zipcode Empty')
            return redirect(create)
        if not request.POST['userName']:
            messages.info(request, 'Username Empty')
            return redirect(create)
        if not request.POST['password']:
            messages.info(request, 'Password Empty')
            return redirect(create)
        if not request.POST['confirm']:
            messages.info(request, 'You must confirm Your password')
            return redirect(create)

        if request.POST['confirm'] == request.POST['password'] :
            messages.info(request, 'The passwords do not match')
            return redirect(create)
        """
        if User.filter(email = request.POST['email']).exists():
            messages.info(request, 'Email Already Used')
            return redirect(create)
        elif Account.objects.filter(username = request.POST['username'] ).exists():
            messages.info(request, 'Username Already Used')
            return redirect(create)
        else:
            return redirect(login)
        """  
    else:
        return redirect(create)

    return redirect(create)
    


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
