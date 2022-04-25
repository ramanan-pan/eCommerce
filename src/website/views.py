
from operator import truediv
from pyexpat.errors import messages
from tkinter.tix import Tree
from turtle import update
from urllib import response
from xml.dom.domreg import registered
from xml.etree.ElementTree import tostring
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from requests import request
from website.EmailBot import EmailBot
from .models import *
import re
from website.cart import Cart
from .models import Book
from yagmail import YagAddressError
from .uitls import TokenGenerator


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
    if request.method=='POST':
        print( request.POST.get('id'))
        res = Reservation.objects.filter(id = request.POST.get('id'))[0]
        res.complete()
    
    reservations = Reservation.objects.filter(expiry__gte = datetime.date.today())
    context = {'reservations' : reservations}
    return render(request, 'website/reservations.html', context)

def expiry(request):
    if request.method=='POST':
        res = Reservation.objects.filter(id = request.POST.get('id'))[0]
        res.delete()

    reservations = Reservation.objects.filter(expiry__lte = datetime.datetime.now())
    context = {'reservations' : reservations}
    return render(request, 'website/expiredreservations.html', context)

def image(request):
    return render(request, 'website/manageusers/turnpike-blur.jpeg')

def conf(request):
    context = {}
    cart = Cart(request)
    context['cart'] = cart
    bot = EmailBot()
    gen = TokenGenerator()
    email = ['Here is your order for the date ' + str(datetime.date.today()) + "..."]
    #basket = [1,2] # Given the books stored as an array of IDs...
    #books = list(Book.objects.filter(id__in=(cart))) 
        #generate a list of the book objects and iterate through them.
    price = cart.get_total_price()
    context['price'] = price
    #for b in books:
    #    price += b.price
    discount = 0
    context['discount'] = discount
    
    if request.POST.get('DISCOUNT'):
        discount = int(request.POST.get('DISCOUNT'))
        context['discount'] = discount
    for item in cart:
        email.append(str(item['book']) + ': ' + str(item['price']) + ' Qty: ' +str(item['qty']) )
        for i in range(item['qty']): # not working, need to figure out how to get these values
            bookSale = BookSale()
            bookSale.bookID = (item['book'])
            bookSale.salePrice = (item['price'])
            bookSale.saleDate = datetime.date.today()
            bookSale.save()
    if request.method == "POST":
        sale = Sale()
        context['sale'] = sale
        sale.address = request.POST.get('ADDR')
        email.append('Shipping Address: ' + sale.address)
        if request.COOKIES.get('username'):
            context['log'] = request.COOKIES.get('username')
            sale.purchaser = User.objects.get(username=request.COOKIES.get('username'))
            em = User.objects.get(username=request.COOKIES.get('username'))
            email.insert(0, 'Hello ' + em.fname + ' ' + em.lname + ', ')
            sale.totalPrice = price + discount + 20
            email.append("You spent a total of " + str(sale.totalPrice))
            email.append("Order #: " + gen.generateOrdernum())
            bot.orderConfirmation(em.email, email)
            sale.save()
            context['sale'] = sale
            address = request.POST.get('ADDR')
            context['address'] = address
            cart.clear()
            cart_user = User.objects.get(username = request.COOKIES.get('username'))
            cBooks =  CartBook.objects.filter(user = cart_user)
            for cBook in cBooks:
                cBook.delete()
        else:



            context['cart'] = cart
            return render(request, 'website/orderconf.html', context)
        cart.clear()   
        context['cart'] = cart 
    return render(request, 'website/orderconf.html', context)

def adset(request):
    if Admin.objects.filter(username=request.session['user']).exists():
        user = Admin.objects.filter(username=request.session['user'])[0]
        return render(request, 'website/addex.html', {'user' : user})
    return render(request, 'website/addex.html') 

def cliset(request):
    if Client.objects.filter(username=request.session['user']).exists():
        user = Client.objects.filter(username=request.session['user'])[0]
        return render(request, 'website/cliset.html', {'user' : user})
    return render(request, 'website/cliset.html') 

def venset(request):
    if Vendor.objects.filter(username=request.session['user']).exists():
        user = Vendor.objects.filter(username=request.session['user'])[0]
        return render(request, 'website/venset.html', {'user' : user})
    return render(request, 'website/venset.html') 

def ordersum(request):
    cart = Cart(request)
    bot = EmailBot()
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
            email = user[0].email
            context['address'] = address
            context['email'] = email
    except:
        context['address'] = ''
        context['email'] = ''
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
            #address = user[0].address
            email = user[0].email
            context['email'] = email
    except:
        context['email'] = ''
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
    context = {}
    cart = Cart(request)
    bot = EmailBot()
    email = ['Here is your order for the date ' + str(datetime.date.today()) + "..."]
    #basket = [1,2] # Given the books stored as an array of IDs...
    #books = list(Book.objects.filter(id__in=(cart))) 
        #generate a list of the book objects and iterate through them.
    price = cart.get_total_price()
    context['price'] = price
    #for b in books:
    #    price += b.price
    discount = 0
    context['discount'] = discount
    if request.POST.get('DISCOUNT'):
        discount = int(request.POST.get('DISCOUNT'))
        context['discount'] = discount
    
    
    if request.method == "POST":
        res = Reservation()
        res.totalPrice = price + discount
        res.expiry = datetime.date.today() + datetime.timedelta(days=6)
        res.purchaser = User.objects.filter(username = request.session['user'])[0]
        res.save()
        context['reservation'] = res
        email.append('Pickup by: ' + str(res.expiry))
        pick_up_date = res.expiry.strftime('%B %d, %Y')
        context['pickup'] = pick_up_date
        em = User.objects.get(username=request.COOKIES.get('username'))
        email.insert(0, 'Hello ' + em.fname + ' ' + em.lname + ', ')
        email.append("Please pay in-store a total of " + str(res.totalPrice))
        for item in cart:
            email.append(str(item['book']) + ': ' + str(item['price']) + ' Qty: ' +str(item['qty']) )
            for i in range(item['qty']):
                rBook = ReservedBook()
                rBook.book = (item['book'])
                rBook.reservation = res
                rBook.save()
        cart.clear()
        cart_user = User.objects.get(username = request.COOKIES.get('username'))
        context['log'] = cart_user.username
        cBooks =  CartBook.objects.filter(user = cart_user)
        for cBook in cBooks:
            cBook.delete()
        
        bot.reserveConfirmation(em.email, email)
        return render(request, 'website/reserveconf.html', context)
    cart.clear()
    return render(request, 'website/reserveconf.html', context)

def adminmain(request):
    return render(request, 'website/adminmain.html')

def vendorset(request):
    return render(request,'website/inventory.html')

def vendview(request):
    return render(request, 'website/vendorview.html')


def reserveSummary(request):
    return render(request, 'website/reserveSummary.html')



def addUser(request):
    user = User()
    bot = EmailBot()
    u = True
    e = True
    c = True
    p = True
    pc = True
    fn = True
    ln = True
    addy = True
    zip = True
    gen = TokenGenerator()

    if request.method == 'POST' and request.POST != None:
        if not request.POST['email']: #checks for an empty user input 
            messages.info(request, 'Email Empty ') # tells the user what is wrong
            e = False
        if not request.POST['firstName']:
            messages.info(request, 'First Name Empty')
            fn = False
        if not request.POST['lastName']:
            messages.info(request, 'Last Name Empty ')
            ln = False
        if not request.POST['city']:
            messages.info(request, 'City Empty')
            c = False
        if not request.POST['address']:
            messages.info(request, 'Address Empty ')
            addy = False
        if not request.POST['zipcode']:
            messages.info(request, 'Zipcode Empty ')
            zip = False
        if not request.POST['userName']:
            messages.info(request, 'Username Empty ')
            u = False
        if not request.POST['password']:
            messages.info(request, 'Password Empty ')
            p = False
        if not request.POST['confirm']:
            messages.info(request, 'You must confirm Your password')
            pc = False

        if not (u and e and p and c and fn and ln and pc and zip and addy):     
            return redirect('http://localhost:8000/website/create')


        if request.POST['confirm'] != request.POST['password'] :
            messages.info(request, 'The passwords do not match')
            return redirect('http://localhost:8000/website/create')
        
        if User.objects.filter(email = request.POST['email']).exists() or Client.objects.filter(email = request.POST['email']).exists() or Vendor.objects.filter(email = request.POST['email']).exists() or Admin.objects.filter(email = request.POST['email']).exists():
            messages.info(request, 'Email Already Used')
            return redirect('http://localhost:8000/website/create')
        elif User.objects.filter(username = request.POST['userName'] ).exists() or Client.objects.filter(username = request.POST['userName'] ).exists() or Vendor.objects.filter(username = request.POST['userName'] ).exists() or Admin.objects.filter(username = request.POST['userName'] ).exists():
            messages.info(request, 'Username Already Used')
            return redirect('http://localhost:8000/website/create')
        else:
            user.fname = request.POST['firstName']
            user.lname = request.POST['lastName']
            user.username = request.POST['userName']
            user.address = request.POST['address'] + ", " +  request.POST['city']+" " +request.POST['state'] + ", " + str(request.POST['zipcode'])
            user.email = request.POST['email']
            user.birthDate = request.POST['DOB']
            user.password = request.POST['password']
            vkey = gen.generateToken()
            user.vkey = vkey
            try:
                bot.confirmAccount(request.POST['firstName'],request.POST['lastName'],request.POST['email'],vkey)
            except Exception:
                return redirect('http://localhost:8000/website/create')

            user.save()

            return redirect('http://localhost:8000/website/verify')
            
    else:

        return redirect('http://localhost:8000/website/editaccount')

    
def create(request):
    return render(request, 'website/create.html')

def createsuccess(request):
    return render(request, 'website/createsuccess.html')

def editaccount(request):
    context = {}
    try: 
        if request.session['user']:
            user = User.objects.filter(username=request.session['user'])[0]
            context['log'] = user
    except:
            render(request, 'website/login.html', context)  
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

    return redirect('http://localhost:8000/website/editaccount')


def changePassword(request):
    users = User.objects.all()
    
    if request.POST != None:
        for user in users:
            try:
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
                        return redirect('http://localhost:8000/website/editaccount')
            except KeyError:
                return redirect('http://localhost:8000/website/editaccount')
    
    return redirect('http://localhost:8000/website/editaccount')


def deleteAccount(request):
    cart = Cart(request)
    users = User.objects.all()
    if request.POST != None:
        for user in users:
            if user.username == request.session['user']:
                response = render(request, 'website/login.html')
                response.delete_cookie('username')
                response.delete_cookie('password')
                cart.clear()
                user.delete()

    return redirect('http://localhost:8000/website/login')
    
def forgotpassword(request):
    return render(request, 'website/forgotpassword.html')

def login(request):

    target = None

    if request.COOKIES.get('username'):

        if User.objects.filter(username=request.COOKIES.get('username')).exists():
            target = User.objects.get(username=request.COOKIES.get('username'))
            if (target.password == request.COOKIES.get('password')):
                request.session['user'] = request.COOKIES.get('username')
                return redirect('http://localhost:8000/website/welcome')


        if Vendor.objects.filter(username=request.COOKIES.get('username')).exists():
            target = Vendor.objects.get(username=request.COOKIES.get('username'))
            if (target.password == request.COOKIES.get('password')):
                request.session['user'] = request.COOKIES.get('username')
                return redirect('http://localhost:8000/website/vendorview')

    
        if Client.objects.filter(username=request.COOKIES.get('username')).exists():
            target = Client.objects.get(username=request.COOKIES.get('username'))
            if (target.password == request.COOKIES.get('password')):
                request.session['user'] = request.COOKIES.get('username')
                return redirect('http://localhost:8000/website/clientview')


        if Admin.objects.filter(username=request.COOKIES.get('username')).exists():
            target = Admin.objects.get(username=request.COOKIES.get('username'))
            if (target.password == request.COOKIES.get('password')):
                request.session['user'] = request.COOKIES.get('username')
                return redirect('http://localhost:8000/website/adminview')
        
        
        
    return render(request, 'website/login.html')
    

def recoveryKey(request):
    return render(request,'website/recoveryKey.html' )


def recoverAccount(request):
    if User.objects.filter(rkey=request.POST['recovery']).exists():
            target = User.objects.get(rkey=request.POST['recovery'])
            if (request.POST['confirm'] == request.POST['password']):
                response = redirect('http://localhost:8000/website/login') 
                target.password = request.POST['password']
                target.rkey = 'empty'
                target.save()
                return response
            else:
                messages.info(request, 'The passwords do not match')
                return redirect('http://localhost:8000/website/recoveryKey')
    else:
        messages.info(request, 'Incorrect Recovery Key')
        return redirect('http://localhost:8000/website/recoveryKey')




def validateCreds(request):

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
            return redirect('http://localhost:8000/website/login')
        if not request.POST['password']:
            messages.info(request, 'Password empty')
            return redirect('http://localhost:8000/website/login')
        

        if User.objects.filter(username=request.POST['username']).exists():
            target = User.objects.get(username=request.POST['username'])
            if target.verified == False:
                messages.info(request, 'PLease verify your account')
                return redirect('http://localhost:8000/website/login')
            if (target.password == request.POST['password']):
                response = redirect('http://localhost:8000/website/welcome') 
                response.set_cookie('username', request.POST['username'],max_age=60*60*60*24*7*4 )
                response.set_cookie('password', request.POST['password'],max_age=60*60*60*24*7*4 )
                request.session['user'] = request.POST['username']
                # load cart
                
                
                cart_user = User.objects.filter(username = request.POST['username'])[0]
                cBooks =  CartBook.objects.filter(user = cart_user)
                booklist = []
                qtylist = []
                for cBook in cBooks:
                    book = get_object_or_404(Book, title = cBook.book)
                    #cart.add(book=book, qty=cBook.qty) 
                    booklist.append(book)
                    qtylist.append(cBook.qty)   
                cart = Cart(request)
                cart.addlist(booklist, qtylist)
                #request.session['cart'] = cart
                
                return response
            else:
                messages.info(request, 'Invalid Password')
                return redirect('http://localhost:8000/website/login')
        
        if Vendor.objects.filter(username=request.POST['username']).exists():
            target = Vendor.objects.get(username=request.POST['username'])
            if (target.password == request.POST['password']):
                response = redirect('http://localhost:8000/website/vendorview') 
                response.set_cookie('username', request.POST['username'],max_age=60*60*60*24*7*4 )
                response.set_cookie('password', request.POST['password'],max_age=60*60*60*24*7*4 )
                request.session['user'] = request.POST['username']
                return response
            else:
                messages.info(request, 'Invalid Password')
                return redirect('http://localhost:8000/website/login')

        if Client.objects.filter(username=request.POST['username']).exists():
            target = Client.objects.get(username=request.POST['username'])
            if (target.password == request.POST['password']):
                response = redirect('http://localhost:8000/website/clientview') 
                response.set_cookie('username', request.POST['username'],max_age=60*60*60*24*7*4 )
                response.set_cookie('password', request.POST['password'],max_age=60*60*60*24*7*4 )
                request.session['user'] = request.POST['username']
                return response
            else:
                messages.info(request, 'Invalid Password')
                return redirect('http://localhost:8000/website/login')

        if Admin.objects.filter(username=request.POST['username']).exists():
            target = Admin.objects.get(username=request.POST['username'])
            if (target.password == request.POST['password']):
                response = redirect('http://localhost:8000/website/adminview') 
                response.set_cookie('username', request.POST['username'],max_age=60*60*60*24*7*4 )
                response.set_cookie('password', request.POST['password'],max_age=60*60*60*24*7*4 )
                request.session['user'] = request.POST['username']
                return response
            else:
                messages.info(request, 'Invalid Password')
                return redirect('http://localhost:8000/website/login')
        
            
    messages.info(request, 'Invalid Credentials')
    return redirect('http://localhost:8000/website/login')


def passwordRecovery(request):
     users = User.objects.all()
     gen = TokenGenerator()

     bot = EmailBot()
     found = False
     if request.POST != None:
        for user in users:
            if request.POST['email'] == user.email:
                found = True
                rkey = gen.generateToken()
                user.rkey = rkey
                user.save()
                bot.recoveryKey(user.email, rkey, user.fname, user.lname)
                messages.info(request, 'Email has been sent')
                return render(request, 'website/forgotpassword.html')
        
        if (found == False):
            messages.info(request, 'Email does not exist')
            return render(request, 'website/forgotpassword.html')


     return render(request, 'website/forgotpassword.html')

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


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
    response = redirect('http://localhost:8000/website/login')
    
        #if request.session['user']:
    if User.objects.filter(username=request.session['user']).exists():   
        print('This is not working!')
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            book_id = int(request.POST.get('id'))
            book_qty = int(request.POST.get('qty'))
            book = get_object_or_404(Book, id = book_id)
            cart.add(book=book, qty=book_qty)
            cartqty = cart.__len__()
            response = JsonResponse({'qty': cartqty})
            return response
    else:
        response = redirect('http://localhost:8000/website/login')
        return response
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

def logout(request):
    # save cart
    
    cart = Cart(request)
    #registeredUser = User.objects.filter(username = request.session['user'])[0]
    for item in cart:
        cBook = CartBook()
        cBook.user = User.objects.filter(username = request.session['user'])[0]
        cBook.book = (item['book'])
        cBook.qty = item['qty']
        cBook.save() 
    
    cart.clear()
    request.session['user'] = None
    response = redirect('http://localhost:8000/website/welcome')
    response.delete_cookie('username')
    response.delete_cookie('password')
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


def verify(request):
    return render(request, 'website/verify.html')


def verifyUser(request):
    user = None
    if request.POST:
        if User.objects.filter(vkey=request.POST['verify']).exists:
            user = User.objects.get(vkey=request.POST['verify'])
            user.verified = True
            user.vkey = 'null'
            user.save()
        else:
            messages.info(request, 'Recovery key given is invalid')
            return redirect('http://localhost:8000/website/verify')
            

    return redirect('http://localhost:8000/website/login')



def editVendor(request):

    if Vendor.objects.filter(username=request.session['user']).exists():
        vendor = Vendor.objects.get(username=request.session['user'])
        if request.POST['firstName']:
            vendor.fname = request.POST['firstName']
            vendor.save()
        if request.POST['lastName']:
            vendor.lname = request.POST['lastName']
            vendor.save()
        if request.POST['email']:
            vendor.email = request.POST['email']
            vendor.save()
        #if request.POST['phone']:
        #    vendor.address = request.POST['phone']
        #    vendor.save()

    return redirect('http://localhost:8000/website/venset', {'user', vendor})

def editVendorPass(request):
    users = Vendor.objects.all()
    
    if request.POST != None:
        for user in users:
            try:
                if user.username == request.session['user']:
                    if user.password != request.POST['oldPassword']:
                        messages.info(request, 'Invalid previous password')
                        return redirect('http://localhost:8000/website/venset')
                    if request.POST['newPassword'] != request.POST['confirm']:
                        messages.info(request, 'Passwords do not match')
                        return redirect('http://localhost:8000/website/venset')
                    else:
                        user.password = request.POST['newPassword']
                        user.save()
                        return redirect('http://localhost:8000/website/venset')
            except KeyError:
                return redirect('http://localhost:8000/website/venset')
    
    return redirect('http://localhost:8000/website/venset')


def editClient(request):
    if Client.objects.filter(username=request.session['user']).exists():
        client = Client.objects.get(username=request.session['user'])
        if request.POST['firstName']:
            client.fname = request.POST['firstName']
            client.save()
        if request.POST['lastName']:
            client.lname = request.POST['lastName']
            client.save()
        if request.POST['email']:
            client.email = request.POST['email']
            client.save()
        #if request.POST['phone']:
        #    vendor.address = request.POST['phone']
        #    vendor.save()

    return redirect('http://localhost:8000/website/cliset', {'client' :  client})


def editClientPass(request):
    users = Client.objects.all()
    
    if request.POST != None:
        for user in users:
            try:
                if user.username == request.session['user']:
                    if user.password != request.POST['oldPassword']:
                        messages.info(request, 'Invalid previous password')
                        return redirect('http://localhost:8000/website/cliset')
                    if request.POST['newPassword'] != request.POST['confirm']:
                        messages.info(request, 'Passwords do not match')
                        return redirect('http://localhost:8000/website/cliset')
                    else:
                        user.password = request.POST['newPassword']
                        user.save()
                        return redirect('http://localhost:8000/website/cliset')
            except KeyError:
                return redirect('http://localhost:8000/website/cliset')
    
    return redirect('http://localhost:8000/website/cliset')
def salesReport(request):
    sales = BookSale.objects.prefetch_related('book').values('bookID__title')
    sales = sales.annotate(total=Sum('salePrice'), count=Count('bookID'))
    print(sales)
    tsold = sales.aggregate(bookssold=Sum('count'))
    trevenue = sales.aggregate(totalrevenue=Sum('total'))
    return render(request, 'website/sales.html', {'sales' : sales, 'tsold' : tsold, 'trevenue' : trevenue})
