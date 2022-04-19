class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, book):
        book_ID = book.id

        if book_ID not in self.cart:
            self.cart[book_ID] = {'price': book.price}

        
        