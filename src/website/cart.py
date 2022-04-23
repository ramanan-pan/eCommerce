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
        self.bookinfo = []

    def add(self, book, qty):
        book_id = str(book.id)
        self.bookinfo.append([book.id,qty])
        if book_id in self.cart:
            self.cart[book_id]['qty'] = qty
        else:
            self.cart[book_id] = {'price': str(book.price), 'qty': qty}

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

        for i in range(len(self.bookinfo)):
            if self.bookinfo == book_id[i]:
                self.bookinfo[i][1] = qty


    def save(self):
        self.session.modified = True

    def getStore(self):
        return self.bookinfo