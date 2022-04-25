from audioop import add
from decimal import Decimal
from website.models import Book

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, book, qty):
        book_id = str(book.id)
        if book_id in self.cart:
            self.cart[book_id]['qty'] = qty
        else:
            self.cart[book_id] = {'price': str(book.price), 'qty': qty}

        self.save()

    def addlist(self, booklist, qtylist):
        for i in range(len(booklist)):
            book_id = str(booklist[i].id)
            #if book_id in self.cart:
            #    self.cart[book_id]['qty'] = qtylist[i]
            #else:
            self.cart[book_id] = {'price': str(booklist[i].price), 'qty': qtylist[i]}
            self.save()
        self.save() 

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.books.filter(id__in=book_ids)
        cart = self.cart.copy()

        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())       

    def delete(self, book):
        book_id = str(book)

        if book_id in self.cart:
            del self.cart[book_id]
            print(book_id)
            self.save()    
    
    def update(self, book, qty):
        book_id = str(book)
        if book_id in self.cart:
            self.cart[book_id]['qty'] = qty
        self.save()


    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.session['cart'] = {}
        self.save()
