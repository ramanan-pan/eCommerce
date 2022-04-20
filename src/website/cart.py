class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, book):
        print('cart.add function works!!')
        book_ID = book.id

        if book_ID not in self.cart:
            self.cart[0] = {'price': str(book.price)}

        self.session.modified = True 

        
        