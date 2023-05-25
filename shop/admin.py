from django.contrib import admin
from shop.models import Product, Contact, Order, OrderUpdate

class MyProduct(admin.ModelAdmin):
    list_display = ('product_name', 'category')

# Register your models here.
admin.site.register(Product, MyProduct)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)