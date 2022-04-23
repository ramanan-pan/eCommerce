from django.contrib import admin
from requests import request
from .models import *

# ADMIN MODELS

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'birthDate', 'email', 
                    'phone', 'address', 'username', 'password',
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
    list_display = ['id', 'emailTitle', 'content', 'scheduledTime', 'attachment']
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
    list_display = ['orderID', 'purchaser', 'totalPrice']
    list_editable = list_display[1:]

@admin.register(BookSale)    
class SoldBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'bookID', 'salePrice']
    list_editable = list_display[1:]

# VENDOR MODELS


class VendorSite(admin.AdminSite):
    site_header = 'Vendor Area'
    site_title = 'Manage Inventory'


vendor_site = VendorSite(name="VendorSitef")  

class VendorBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'ISBN', 'genre', 'price', 
                    'numSold', 'picture', 'description','slug','in_stock','stock','created','updated']
    #list_editable = ['title', 'author', 'ISBN', 'genre', 'price', 
    #                'numSold', 'picture', 'description','slug','in_stock','stock','created','updated']
    #list_filter = ['in_stock']
    #prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        return Book.objects.filter(created_by = request.user)

vendor_site.register(Book, VendorBookAdmin)


# CLIENT MODELS

class ClientSite(admin.AdminSite):
    site_header = 'Client Area'

    
client_site = ClientSite(name="ClientSitef")  

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

client_site.register(Book, ClientBookAdmin)

