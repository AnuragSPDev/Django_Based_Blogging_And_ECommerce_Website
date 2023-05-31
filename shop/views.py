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
    return render(request, 'shop/index.html', params)

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
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        try:
            return get_order_updates(order_id, email)
        except Exception:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def get_order_updates(order_id, email):
    order = Order.objects.filter(order_id=order_id, email=email)
    if len(order) <= 0:
        return HttpResponse('{}')
    order_update = OrderUpdate.objects.filter(order_id=order_id)
    updates = []
    for update in order_update:
        updates.append({'text': update.update_desc, 'update_time':update.update_time})
        response = json.dumps(updates, default=str)
    return HttpResponse(response)

def productview(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'shop/productview.html', {'product': product[0]})

def checkout(request):
    if request.method != 'POST':
        return render(request, 'shop/checkout.html')
    error_msg = ''
    
    f_name = request.POST.get('inputFName')
    l_name =  request.POST.get('inputLName')
    name = f'{f_name} {l_name}'
    if not name.strip():
        error_msg += "Name can't be left blank. "
    
    phone = request.POST.get('inputPhone')
    if not phone:
        error_msg += "Phone can't be left blank. "
    
    email = request.POST.get('inputEmail')
    if not email:
        error_msg += "Email can't be left blank. "
    
    address_1 = request.POST.get('inputAddress')
    address_2 = request.POST.get('inputAddress2')
    address = f'{address_1} {address_2}'
    if not address.strip():
        error_msg += "Address can't be left blank. "
    
    city = request.POST.get('inputCity')
    if not city:
        error_msg += "City can't be left blank. "
    
    state = request.POST.get('inputState')
    if not state:
        error_msg += "State can't be left blank. "
    
    zip_code = request.POST.get('inputZip')
    if not zip_code:
        error_msg += "Zip code can't be left blank. "
    
    items_json = request.POST.get('items_json')
    
    if error_msg:
        return render(request, 'shop/checkout.html', {'error_msg':error_msg})
    
    order = Order(name=name, phone=phone, email=email, address=address, city=city, state=state,
                  zip_code=zip_code, items_json=items_json)

    order.save()

    # when an order has been placed, update the OrderUpdate table to reflect the initial update
    # that an order has been placed.
    initial_update = OrderUpdate(order_id=order.order_id, update_desc = 'Your order has been placed.')
    initial_update.save()

    order_id = order.order_id

    
    order_placed = True
    return render(request, 'shop/checkout.html ', {'order_placed':order_placed, 'order_id':order_id, 'error_msg':error_msg})