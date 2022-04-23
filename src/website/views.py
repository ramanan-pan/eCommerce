
from pyexpat.errors import messages
from turtle import update
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.http import JsonResponse
from website.EmailBot import EmailBot
from .models import *
import re
from website.cart import Cart
from .models import Book


# Create your views here.
def index(request):
    books = Book.objects.all()


    
    if request.method == 'GET':
        query = request.GET.get('q')
        searchbutton = request.GET.get('submit')
        options = request.GET.get('options')
        
        if query is not None:
            if options == 'title':
                lookups = Q(title__icontains = query)
            elif options == 'author':
                lookups = Q(author__icontains = query)
            elif options == 'isbn':
                lookups = Q(ISBN__icontains = query)
            elif options == 'subject':
                lookups = Q(genre__icontains = query)
            else: 
                lookups = Q(title__icontains = query) | Q(description__icontains = query)
            results = books.filter(lookups).distinct()
            context={'results': results,
                     'searchbutton': searchbutton,
                     'options' : options,
                     'books': books
                     }
            try: 
                if request.session['user']:
                    user = User.objects.filter(username=request.session['user'])
                    context['log'] = user
            except:
                context['log'] = ''
            return render(request, 'website/index.html', context)  
        else: 
            context = {'books' : books}
            try: 
                if request.session['user']:
                    user = User.objects.filter(username=request.session['user'])
                    context['log'] = user
            except:
                context['log'] = ''
            return render(request, 'website/index.html', context)
    else:
        context = {'books' : books}
        try: 
            if request.session['user']:
                user = User.objects.filter(username=request.session['user'])
                context['log'] = user
        except:
            context['log'] = ''
        return render(request, 'website/index.html', context)
        

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, in_stock=True)
    context = {'book' : book}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''
    return render(request, 'website/books/detail.html',  context)

def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug, in_stock=True)
    if request.method=='POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.price = request.POST.get('price')
        book.genre = request.POST.get('genre')
        book.stock = request.POST.get('stock')
        book.save()
        message = "The book has been updated."
        return render(request, 'website/books/edit.html', {'book' : book, 'message' : message})
    return render(request, 'website/books/edit.html', {'book': book})
    
def welcome(request):
    books = Book.objects.all()
    context = {'books' : books}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''
    return render(request, 'website/welcome.html', context)


def cv(request):
    return render(request, 'website/ClientView.html')

def home(request):
    return render(request, 'website/home.html')

def res(request):
    return render(request, 'website/reservations.html')

def expiry(request):
    return render(request, 'website/expiredreservations.html')

def image(request):
    return render(request, 'website/manageusers/turnpike-blur.jpeg')

def conf(request):
    cart = Cart(request)
    #basket = [1,2] # Given the books stored as an array of IDs...
    #books = list(Book.objects.filter(id__in=(cart))) 
        #generate a list of the book objects and iterate through them.
    price = cart.get_total_price()
    #for b in books:
    #    price += b.price
    discount = 0
    if request.POST.get('DISCOUNT'):
        discount = int(request.POST.get('DISCOUNT'))
    for item in cart:
        for i in range(item['qty']): # not working, need to figure out how to get these values
            bookSale = BookSale()
            bookSale.bookID = (item['book'])
            bookSale.salePrice = (item['price'])
            bookSale.saleDate = datetime.date.today()
            bookSale.save()
    if request.method == "POST":
        sale = Sale()
        if request.COOKIES.get('username'):
            sale.purchaser = request.COOKIES.get('username')
        else:
            sale.purchaser = request.POST.get('CARD') #TODO switch with user ID
        sale.totalPrice = price + discount + 20
        sale.save()
        address = request.POST.get('ADDR')
        
        request.session['cart'] = {}
        return render(request, 'website/orderconf.html', {'price' : price, 'cart' : cart, 'sale' : sale, 'discount' : discount, "addr" : address})
    return render(request, 'website/orderconf.html', {'price' : price})

def adset(request):
    return render(request, 'website/addex.html') 

def cliset(request):
    return render(request, 'website/cliset.html') 

def venset(request):
    return render(request, 'website/venset.html') 

def ordersum(request):
    cart = Cart(request)
    #basket = [1,2]
    #books = list(Book.objects.filter(id__in=(basket)))
    price = cart.get_total_price()
    #for b in books:
    #    price += b.price
    context = {'cart' : cart}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            address = user[0].address
            context['address'] = address
    except:
        context['address'] = ''
    if request.method == "POST" and request.POST.get('CODE'):
        discount = 0
        try:
            promo = Promotion.objects.filter(code=request.POST.get('CODE'))[0]
            if promo.pctdiscount:
                discount = -price*promo.pctdiscount
                discount = int(discount/100)
            else:
                discount = -promo.amountdiscount
        finally:
            context['discount'] = discount
            context['price'] = price
            return render(request, 'website/ordersummary.html', context)
    #TODO get the list of books from the user session.
    context['price'] = price
    return render(request, 'website/ordersummary.html', context)

def reservesum(request):
    cart = Cart(request)
    #basket = [1,2]
    #books = list(Book.objects.filter(id__in=(basket)))
    price = cart.get_total_price()
    #for b in books:
    #    price += b.price
    context = {'cart' : cart}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            address = user[0].address
            context['address'] = address
    except:
        context['address'] = ''
    if request.method == "POST" and request.POST.get('CODE'):
        discount = 0
        try:
            promo = Promotion.objects.filter(code=request.POST.get('CODE'))[0]
            if promo.pctdiscount:
                discount = -price*promo.pctdiscount
                discount = int(discount/100)
            else:
                discount = -promo.amountdiscount
        finally:
            context['discount'] = discount
            context['price'] = price
            return render(request, 'website/reserveSummary.html', context)
    #TODO get the list of books from the user session.
    context['price'] = price
    return render(request, 'website/reserveSummary.html', context)


def reserveconf(request):
    cart = Cart(request)
    #basket = [1,2] # Given the books stored as an array of IDs...
    #books = list(Book.objects.filter(id__in=(cart))) 
        #generate a list of the book objects and iterate through them.
    price = cart.get_total_price()
    #for b in books:
    #    price += b.price
    discount = 0
    if request.POST.get('DISCOUNT'):
        discount = int(request.POST.get('DISCOUNT'))
    '''
    for item in cart:
        for i in range(item['qty']): # not working, need to figure out how to get these values
            bookSale = BookSale()
            bookSale.bookID = (item['book'])
            bookSale.salePrice = (item['price'])
            bookSale.saleDate = datetime.date.today()
            bookSale.save()
    if request.method == "POST":
        sale = Sale()
        if request.COOKIES.get('username'):
            sale.purchaser = request.COOKIES.get('username')
        else:
            sale.purchaser = request.POST.get('CARD') #TODO switch with user ID
        sale.totalPrice = price + discount + 20
        sale.save()
        address = request.POST.get('ADDR')
        
        request.session['cart'] = {}
        return render(request, 'website/orderconf.html', {'price' : price, 'cart' : cart, 'sale' : sale, 'discount' : discount, "addr" : address})
        '''
    return render(request, 'website/reserveconf.html', {'price' : price, 'cart': cart, 'discount': discount})

def adminmain(request):
    return render(request, 'website/adminmain.html')

def vendorset(request):
    return render(request,'website/inventory.html')

def vendview(request):
    return render(request, 'website/vendorview.html')



def addUser(request):
    user = User()
    bot = EmailBot()

    if request.method == 'POST' and request.POST != None:
        if not request.POST['email']: #checks for an empty user input 
            messages.info(request, ' Email Empty') # tells the user what is wrong
            return render(request, 'website/create.html') #returns user back to the creation screen
        if not request.POST['firstName']:
            messages.info(request, ' First Name Empty')
            return render(request, 'website/create.html')
        if not request.POST['lastName']:
            messages.info(request, 'Last Name Empty')
            return render(request, 'website/create.html')
        if not request.POST['address1']:
            messages.info(request, 'Address 1 Empty')
            return render(request, 'website/create.html')
        if not request.POST['address2']:
           messages.info(request, 'Adress 2 Empty')
           return render(request, 'website/create.html')
        if not request.POST['zipcode']:
            messages.info(request, 'Zipcode Empty')
            return render(request, 'website/create.html')
        if not request.POST['userName']:
            messages.info(request, 'Username Empty')
            return render(request, 'website/create.html')
        if not request.POST['password']:
            messages.info(request, 'Password Empty')
            return render(request, 'website/create.html')
        if not request.POST['confirm']:
            messages.info(request, 'You must confirm Your password')
            return render(request, 'website/create.html')

        if request.POST['confirm'] != request.POST['password'] :
            messages.info(request, 'The passwords do not match')
            return render(request, 'website/create.html')
        
        if User.objects.filter(email = request.POST['email']).exists() or Client.objects.filter(email = request.POST['email']).exists() or Vendor.objects.filter(email = request.POST['email']).exists() or Admin.objects.filter(email = request.POST['email']).exists():
            messages.info(request, 'Email Already Used')
            return render(request, 'website/create.html')
        elif User.objects.filter(username = request.POST['userName'] ).exists() or Client.objects.filter(username = request.POST['userName'] ).exists() or Vendor.objects.filter(username = request.POST['userName'] ).exists() or Admin.objects.filter(username = request.POST['userName'] ).exists():
            messages.info(request, 'Username Already Used')
            return render(request, 'website/create.html')
        else:
            user.fname = request.POST['firstName']
            user.lname = request.POST['lastName']
            user.username = request.POST['userName']
            user.address = request.POST['address1']
            user.email = request.POST['email']
            user.birthDate = request.POST['DOB']
            user.password = request.POST['password']
            bot.confirmAccount(request.POST['firstName'],request.POST['lastName'],request.POST['email'] )
            user.save()

            return render(request, 'website/login.html')
            
    else:
        return render(request, 'website/create.html')

    
def create(request):
    return render(request, 'website/create.html')

def createsuccess(request):
    return render(request, 'website/createsuccess.html')

def editaccount(request):
    context = {}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''  
    return render(request, 'website/editaccount.html', context)

def changeAccount(request):
    users = User.objects.all()

    if request.POST != None:
        for user in users:
            if user.username == request.session['user']:
                user = User.objects.get(id=user.id)
                if request.POST['firstName']:
                    user.fname = request.POST['firstName']
                    user.save()
                if request.POST['lastName']:
                    user.lname = request.POST['lastName']
                    user.save()
                if request.POST['email']:
                    user.email = request.POST['email']
                    user.save()
                if request.POST['address1']:
                    user.address = request.POST['address1']
                    user.save()
                if request.POST['zipcode']:
                    user.zipcode = request.POST['zipcode']
                    user.save()

    context = {}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''                

    return render(request, 'website/editaccount.html', context)


def changePassword(request):
    users = User.objects.all()
    if request.POST != None:
        for user in users:
            if user.username == request.session['user']:
                if user.password != request.POST['oldPassword']:
                    messages.info(request, 'Invalid previous password')
                    return render(request, 'website/editaccount.html')
                if request.POST['newPassword'] != request.POST['confirm']:
                    messages.info(request, 'Passwords do not match')
                    return render(request, 'website/editaccount.html')
                else:
                    user.password = request.POST['newPassword']
                    user.save()
    
    context = {}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''
    return render(request, 'website/editaccount.html', context)


def deleteAccount(request):
    users = User.objects.all()
    if request.POST != None:
        for user in users:
            if user.username == request.session['user']:
                response = render(request, 'website/login.html')
                response.delete_cookie('username')
                response.delete_cookie('password')
                user.delete()

    return render(request, 'website/login.html')
    
def forgotpassword(request):
    return render(request, 'website/forgotpassword.html')

def login(request):
    users = User.objects.all()
    vendors = Vendor.objects.all()
    admins = Admin.objects.all()
    clients = Client.objects.all()

    for user in users:
        if request.COOKIES.get('username') == user.username and request.COOKIES.get('password') == user.password:
            request.session['cart'] = {}
            request.session['user'] = request.COOKIES.get('username')
            return render(request, 'website/welcome.html')
        

   

    for client in clients:
        if request.COOKIES.get('username') == client.username and request.COOKIES.get('password') == client.password:
            request.session['cart'] = {}
            request.session['user'] = request.COOKIES.get('username')
            return render(request, 'website/ClientView.html')
        
            

    for vendor in vendors:
        if request.COOKIES.get('username') == vendor.username and request.COOKIES.get('password') == vendor.password:
            request.session['cart'] = {}
            request.session['user'] = request.COOKIES.get('username')
            return render(request, 'website/welcome.html')
        
            

    for admin in admins:
        if request.COOKIES.get('username') == admin.username and request.COOKIES.get('password') == admin.password:
            request.session['cart'] = {}
            request.session['user'] = request.COOKIES.get('username')
            return render(request, 'website/adminmain.html')
        
        
    return render(request,'website/login.html' )
    


def validateCreds(request):
    
    foundU = False
    foundV = False
    foundA = False
    foundC = False
    
    users = User.objects.all()
    vendors = Vendor.objects.all()
    admins = Admin.objects.all()
    clients = Client.objects.all()


    books = Book.objects.all()
    context = {'books' : books}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''  

    if request.POST != None:
        if not request.POST['username']:
            messages.info(request, 'Username empty')
            return render(request, 'website/login.html')
        if not request.POST['password']:
            messages.info(request, 'Password empty')
            return render(request, 'website/login.html')
        

        for user in users:
            if request.POST['username'] == user.username and request.POST['password'] == user.password:
                foundU = True
            else:
                print('NO')

        for vendor in vendors:
            if request.POST['username'] == vendor.username and request.POST['password'] == vendor.password:
                foundV = True
            else:
                print('NO')

        for client in clients:
            if request.POST['username'] == client.username and request.POST['password'] == client.password:
                foundC = True
            else:
                print('NO')


        for admin in admins:
            if request.POST['username'] == admin.username and request.POST['password'] == admin.password:
                foundA = True
            else:
                print('NO')
        
        if (foundU):
            if (request.POST.get('box') == 'checked'):
                response = render(request, 'website/welcome.html', context)
                response.set_cookie('username', request.POST['username'], max_age=60*60*10*4*7*4) # the cookie will stay for 46 days
                response.set_cookie('password', request.POST['password'], max_age=60*60*10*4*7*4)
                request.session['cart'] = {} 
                request.session['user'] = request.POST['username']
                return response
            else:
                request.session['user'] = request.POST['username']
                return render(request, 'website/welcome.html', context)
        
        elif (foundV):
            if (request.POST.get('box') == 'checked'):
                response = render(request, 'website/vendorview.html')
                response.set_cookie('username', request.POST['username'], max_age=60*60*10*4*7*4) # the cookie will stay for 46 days
                response.set_cookie('password', request.POST['password'], max_age=60*60*10*4*7*4)
                request.session['cart'] = {} 
                request.session['user'] = request.POST['username']
                return response
            else:
                request.session['user'] = request.POST['username']
                return render(request, 'website/vendorview.html')
        elif (foundA):
            if (request.POST.get('box') == 'checked'):
                response = render(request, 'website/adminmain.html')
                response.set_cookie('username', request.POST['username'], max_age=60*60*10*4*7*4) # the cookie will stay for 46 days
                response.set_cookie('password', request.POST['password'], max_age=60*60*10*4*7*4)
                request.session['cart'] = {} 
                request.session['user'] = request.POST['username']
                return response
            else:
                request.session['user'] = request.POST['username']
                return render(request, 'website/adminmain.html')
        elif (foundC):
            if (request.POST.get('box') == 'checked'):
                response = render(request, 'website/ClientView.html')
                response.set_cookie('username', request.POST['username'], max_age=60*60*10*4*7*4) # the cookie will stay for 46 days
                response.set_cookie('password', request.POST['password'], max_age=60*60*10*4*7*4)
                request.session['cart'] = {} 
                request.session['user'] = request.POST['username']
                return response
            else:
                request.session['user'] = request.POST['username']
                return render(request, 'website/ClientView.html')
        else:
            messages.info(request, 'Invalid Login')
            return render(request, 'website/login.html')

    return render(request, 'website/login.html')


def passwordRecovery(request):
     users = User.objects.all()
     bot = EmailBot()
     found = False
     if request.POST != None:
        for user in users:
            if request.POST['email'] == user.email:
                found = True
                bot.recoveryPass(user.email, user.fname, user.lname, user.password)
                messages.info(request, 'Email has been sent')
                return render(request, 'website/forgotpassword.html')
        
        if (found == False):
            messages.info(request, 'Email does not exist')
            return render(request, 'website/forgotpassword.html')


     return render(request, 'website/forgotpassword.html')


def recoversent(request):
    return render(request, 'website/recoversent.html')

def cart(request):
    cart = Cart(request)
    context = {'cart' : cart}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])
            context['log'] = user
    except:
            context['log'] = ''
    return render(request, 'website/cart.html', context)

def viewBook(request):
    return render(request, 'website/viewBook.html')

def mangusers(request):
    return render(request, 'website/manageusers.html')

def mangord(request):
    return render(request, 'website/manageorders.html')

def mangvend(request):
    return render(request, 'website/managevendors.html')

def mangprom(request):
    return render(request, 'website/managepromotions.html')

def manadmin(request):
    return render(request, 'website/copyinventory.html')

#Gets a queryset of all books under this vendor's username.  Assumes
#that the given vendor username is correct.
def getBooksByVendor(vendorName):
    books = Book.objects.filter(created_by_id = Vendor.objects.filter(username = vendorName)[0].id)
    return books
    
def cart_add(request):
    #print('cart_add is called')
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('id'))
        book_qty = int(request.POST.get('qty'))
        book = get_object_or_404(Book, id = book_id)
        cart.add(book=book, qty=book_qty)
        cartqty = cart.__len__()
        response = JsonResponse({'qty': cartqty})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('id'))
        cart.delete(book=book_id)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('id'))
        book_qty = int(request.POST.get('qty'))
        cart.update(book=book_id, qty=book_qty)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response

#TODO integrate with login when it's fixed
def inventory(request):
    books = []
    
    user = request.session['user']
    acct = None
    if Vendor.objects.filter(username = user):
        books = getBooksByVendor(user)
        acct = Vendor.objects.filter(username = user)[0]
    elif Admin.objects.filter(username = user):
        books = Book.objects.all()
        acct = Admin.objects.filter(username = user)
    price = sumPrice(books)
    return render(request, 'website/inventory.html',{'books' : books, 'price' : price, 'acct' : acct})
    

def sumPrice(books):
    price = 0
    for b in books:
        price += b.price
    return price