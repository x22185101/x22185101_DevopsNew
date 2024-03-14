from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, CartItem, Order
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import requests

API_GATEWAY_ENDPOINT = 'https://l556xhz8fh.execute-api.us-east-2.amazonaws.com/dev'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'pet_products/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pet_products:pet_products')
    else:
        form = ProductForm()
    return render(request, 'pet_products/add_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to add items to your cart.')
        return redirect('users:sign_in')

    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('pet_products:view_cart')
    
@login_required
def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to remove items from your cart.')
        return redirect('users:sign_in')

    product = get_object_or_404(Product, pk=product_id)
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('pet_products:view_cart')

@login_required
def place_order(request):
    print("Place Order View Reached")
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items:
        order = Order.objects.create(user=request.user)
        order.items.set(cart_items)

        invoice_data = {}
        for item in cart_items:
            # Convert decimal price to float
            invoice_data[item.product.name] = float(item.product.price)

        payload = {
            'invoice_data': {
                'customer': request.user.username,  # Assuming username is the customer identifier
                'products': invoice_data
            }
        }

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(API_GATEWAY_ENDPOINT, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            messages.success(request, f"Your order has been placed. {result['message']}")
        except requests.RequestException as e:
            messages.error(request, f"Failed to place order: {e}")

        cart_items.delete()

        print("Redirecting to order_confirmation")
        return redirect('pet_products:order_confirmation')

    print("Redirecting to pet_products")
    return redirect('pet_products:pet_products')







def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'pet_products/cart.html', {'cart_items': cart_items})
    
def order_confirmation(request):
    return render(request, 'pet_products/order_confirmation.html')







