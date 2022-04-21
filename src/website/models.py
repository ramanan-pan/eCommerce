from django.db.models import *
from django.core.exceptions import ValidationError
import datetime
from django.urls import reverse
# Create your models here.

class Account(Model):
    fname = CharField(max_length=255)
    lname = CharField(max_length=255)
    newsletters = BooleanField(default=True)
    subscriptions = BooleanField(default=True)
    username = CharField(max_length=40, unique=True)
    password = CharField(max_length=255)
    email = CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        abstract = True

class User(Account):
    #TODO decomp into account, and inherit from account
    birthDate = DateField()
    phone = IntegerField(max_length=10, blank=True, null=True)
    address = CharField(max_length=255)

class Vendor(Account):
    None

class Client(Account):
    organizationName = CharField(max_length=255)

class Admin(Account):
    None
    
    def __str__(self):
        return self.username

class Promotion(Model):
    name = CharField(max_length=255)
    description = CharField(max_length=255, blank=True)
    startdate = DateField()
    enddate = DateField()
    def serial_date(self):
        if (self.enddate < self.startdate):
            raise ValidationError("End date is after start date")
    code = CharField(max_length=24, unique=True)
    pctdiscount = IntegerField(max_length=4, blank=True, null=True)
    amountdiscount = IntegerField(max_length=6, blank=True, null=True)
    def has_discount(self):
        if (self.pctdiscount is None and self.amountdiscount is None):
            raise ValidationError("Must enter either a percent or amount discount")
        if (self.pctdiscount is not None and self.amountdiscount is not None):
            raise ValidationError("Must choose either a percentage or amount discount, not both")
    
    def __str__(self):
        return self.code

    def clean(self):
        self.serial_date()
        self.has_discount()

class NewsLetter(Model):
    emailTitle = CharField(max_length=255)
    content = CharField(max_length=255)
    scheduledTime = DateField()
    attachment = CharField(max_length=255)


class BookManager(Manager):
    def get_queryset(self):
        return super(BookManager, self).get_queryset().filter(is_active=True)


class Book(Model):
    id = AutoField(primary_key=True)
    created_by = ForeignKey(Vendor, on_delete=CASCADE, related_name='book_creator')
    price = DecimalField(max_digits=6, decimal_places=2)
    author = CharField(max_length=255)
    ISBN = IntegerField(unique=True)
    title = CharField(max_length=255)
    genre = CharField(max_length=255)
    numSold = IntegerField(default=0)
    picture = CharField(max_length=255, blank=True)
    slug = SlugField(max_length=255)
    description = TextField(blank=True)
    in_stock = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    objects = Manager()
    books = BookManager()

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('website:website-book_detail', args=[self.slug])

    def __str__(self):
        return self.title

class Sale(Model):
    orderID = AutoField(primary_key=True)
    purchaser = CharField(max_length=255) #For now, saving CC number
    #purchaser = ForeignKey(User, on_delete=CASCADE)
    totalPrice = IntegerField()

class BookSale(Model):
    bookID = ForeignKey(Book, related_name="bookID", on_delete=CASCADE)
    salePrice = IntegerField()
    saleDate = DateField(default=datetime.date.today())




