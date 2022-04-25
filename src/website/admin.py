from django.contrib import admin
from requests import request
from .models import *
from django.contrib.admin.models import LogEntry

# ADMIN MODELS

admin.site.site_url = '/website/adminview'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'birthDate', 'email', 
                    'phone', 'address', 'username', 'password', 'rkey', 'vkey', 'verified',
                    'newsletters', 'subscriptions']
    list_editable = list_display[1:]

@admin.register(Vendor)    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'email',
                    'username', 'password',
                    'newsletters', 'subscriptions']
    list_editable = list_display[1:]

@admin.register(Client)    
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'email',
                    'username', 'password',
                    'newsletters', 'subscriptions',
                    'organizationName']
    list_editable = list_display[1:]

@admin.register(Admin)    
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'email',
                    'username', 'password',
                    'newsletters', 'subscriptions']
    list_editable = list_display[1:]

@admin.register(Promotion)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'startdate', 'enddate',
                    'code', 'pctdiscount', 'amountdiscount']
    list_editable = list_display[1:]

@admin.register(NewsLetter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['id', 'emailTitle', 'content']
    list_editable = list_display[1:]

@admin.register(Book)    
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author','created_by' ,'ISBN', 'genre', 'price', 
                    'numSold', 'picture', 'description','slug','in_stock','created','updated']
    list_editable = list_display[1:]
    list_filter = ['in_stock']
    list_editable = ['price','in_stock']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Sale)    
class SaleAdmin(admin.ModelAdmin):
    list_display = ['orderID', 'purchaser', 'name','address','date','totalPrice']
    list_editable = list_display[1:]

@admin.register(BookSale)    
class SoldBookAdmin(admin.ModelAdmin):
    list_display = ['id','sale', 'bookID', 'salePrice', 'saleDate']
    list_editable = list_display[1:]

@admin.register(ReservedBook)
class ReservedBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'reservation']
    list_editable = list_display[1:]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchaser', 'totalPrice', 'expiry']
    list_editable = list_display[1:]

@admin.register(CartBook)
class CartBookAdmin(admin.ModelAdmin):
    list_display = ['id','book','user','qty']
    list_editable = list_display[1:]
    
# VENDOR MODELS


class VendorSite(admin.AdminSite):
    site_header = 'Vendor Area'
    site_title = 'Admin'
    site_url = '/website/vendorview'
    index_title = 'Manage Inventory'
    LogEntry.objects.all().delete()


vendorSite = VendorSite(name="vendorSite")  

class VendorBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'ISBN', 'genre', 'price', 
                    'numSold', 'picture', 'description','slug','in_stock','stock','created','updated']
    #list_editable = ['title', 'author', 'ISBN', 'genre', 'price', 
    #                'numSold', 'picture', 'description','slug','in_stock','stock','created','updated']
    #list_filter = ['in_stock']
    #prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        vendor = Vendor.objects.filter(username=request.session['user'])[0]
        #vendor
        return Book.objects.filter(created_by = vendor)

vendorSite.register(Book, VendorBookAdmin)


# CLIENT MODELS

class ClientSite(admin.AdminSite):
    site_header = 'Client Area'
    site_title = 'Admin'
    site_url = '/website/clientview'
    index_title = 'View Inventory'
    LogEntry.objects.all().delete()

    
clientSite = ClientSite(name="clientSite")  

class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ClientBookAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ['title', 'author', 'created_by' ,'ISBN', 'genre', 'price', 
                    'numSold', 'picture', 'description','slug','in_stock','stock','created','updated']

clientSite.register(Book, ClientBookAdmin)

