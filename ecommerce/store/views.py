from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime

from .utils import cookieCart, cartData, guestOrder

def store(request):

    data= cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    
    data= cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/cart.html", context)

def checkout(request):

    data= cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/checkout.html", context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data= json.loads(request.body)
    # parse the data
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
      
    else:
        customer , order = guestOrder(request , data)
       
        total = float(data['form']['total'])  # Assuming 'total' is directly in 'data' dictionary
        order.transaction_id = transaction_id
        
        if total == float(order.get_cart_total):  # Corrected: Method name and variable usage
            order.complete = True
        order.save()

        if order.shipping == True:
            # Assuming correct structure of form data, adjust as needed
            ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode']
            )


    return JsonResponse({'message': 'Payment complete'}, safe=False)


def updateItem(request):
    # post request we are sending
    data= json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created= OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity= (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)
