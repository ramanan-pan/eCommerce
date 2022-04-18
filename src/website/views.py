from django.shortcuts import render
from django.template import RequestContext
from .models import *

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

