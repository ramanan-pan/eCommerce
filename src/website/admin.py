from django.contrib import admin
from .models import *

# Register your models here.

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
    list_display = ['id', 'title', 'author', 'ISBN', 'genre', 'price', 
                    'numSold', 'picture', 'description','slug','in_stock','created','updated']
    list_editable = list_display[1:]
    list_filter = ['in_stock']
    list_editable = ['price','in_stock']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Sale)    
class SaleAdmin(admin.ModelAdmin):
    list_display = ['orderID', 'purchaser', 'totalPrice']
    list_editable = list_display[1:]
