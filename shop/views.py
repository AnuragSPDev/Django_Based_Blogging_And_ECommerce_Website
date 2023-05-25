from itertools import product
from math import ceil
from django.shortcuts import render, HttpResponse
from shop.models import Product, Contact, Order, OrderUpdate
from django.contrib import messages
import json

# Create your views here.
def index(request):
    all_products = []
    all_categories = Product.objects.values('category')
    product_category = {item['category'] for item in all_categories}
    print(product_category)
    for category in product_category:
        products = Product.objects.filter(category = category) 
        n = len(products)
        # to calculate how many slieds on the page
        # as we have 4 cards per slide then below formula derives how many 
        # slides do we need to have on the page in order to display our 
        # products.
        num_of_slides = n//4 + ceil((n/4) - (n//4))
        all_products.append([products, range(1, num_of_slides), num_of_slides])

    params = {'all_products': all_products}
    return render(request, 'shop/in+dex.html', params)

def about(request):
    return render(request, 'shop/aboutus.html')

def contact(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        print(f'{username}, {email}, {phone}, {desc}')
        contact = Contact(name=username, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, 'Your quey has been sent successfully')
        render(request, 'shop/contactus.html')

    return render(request, 'shop/contactus.html')

def search(request):
    return render(request, 'shop/search.html')

def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderId')
        email = request.POST.get('inputEmail')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                order_update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for update in order_update:
                    updates.append({'text': update.update_desc, 'update_time':update.update_time})
                    response = json.dumps(updates)
                    return HttpResponse(response)
            else:
                return HttpResponse('error')
        except:
            return HttpResponse('exception')

    return render(request, 'shop/tracker.html')

def productview(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'shop/productview.html', {'product': product[0]})

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('inputFName') + ' ' +  request.POST.get('inputLName')
        phone = request.POST.get('inputPhone')
        email = request.POST.get('inputEmail')
        address = request.POST.get('inputAddress') + ' ' + request.POST.get('inputAddress2')
        city = request.POST.get('inputCity')
        state = request.POST.get('inputState')
        zip_code = request.POST.get('inputZip')
        items_json = request.POST.get('items_json')
        order = Order(name=name, phone=phone, email=email, address=address, city=city, state=state,
                      zip_code=zip_code, items_json=items_json)
        
        order.save()

        # when an order has been placed, update the OrderUpdate table to reflect the initial update
        # that an order has been placed.
        initial_update = OrderUpdate(order_id=order.order_id, update_desc = 'Your order has been placed.')
        initial_update.save()

        order_placed = True
        order_id = order.order_id

        return render(request, 'shop/checkout.html', {'order_placed':order_placed, 'order_id':order_id})
    
    return render(request, 'shop/checkout.html')