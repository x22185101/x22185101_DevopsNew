from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, CartItem, Order
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import requests
from django.http import HttpResponse
import os
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal

API_GATEWAY_ENDPOINT = 'https://l556xhz8fh.execute-api.us-east-2.amazonaws.com/dev'
S3_BUCKET = '22185101-pdf-upload'
COUPON_API = 'https://qjc1v6hvs1.execute-api.sa-east-1.amazonaws.com/X22239243_CouponCodes'

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
            invoice_data[item.product.name] = {
                'price': float(item.product.price),
                'quantity': item.quantity  # Include the quantity in the invoice data
            }
 
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
            print("Response:", response.text)  # Print the response content for debugging
            response_json = response.json()  # Parse JSON response
            print("Response JSON:", response_json)  # Print the parsed JSON for debugging
 
            invoice_url = response_json.get('s3_url')  # Get the S3 URL from the response
            if invoice_url:
                print(f"Invoice Url: {invoice_url}")
                messages.success(request, "Your order has been placed. Invoice saved.")
                cart_items.delete()
  
                # Pass invoice_url to order_confirmation view
                return redirect(reverse('pet_products:order_confirmation') + f'?invoice_url={invoice_url}')
            else:
                messages.error(request, "Failed to retrieve invoice URL.")
        except requests.RequestException as e:
            messages.error(request, f"Failed to place order: {e}")
 
        cart_items.delete()
 
        print("Redirecting to pet_products")
        return redirect('pet_products:pet_products')
 
    print("Redirecting to pet_products")
    return redirect('pet_products:pet_products')

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'pet_products/cart.html', {'cart_items': cart_items})
    
def order_confirmation(request):
    invoice_url = request.GET.get('invoice_url')
    return render(request, 'pet_products/order_confirmation.html', {'invoice_url': invoice_url})

@user_passes_test(lambda u: u.is_staff)
def coupon(request):
    try:
        response = requests.post(COUPON_API, json={'operation': 'get_coupon_details'})
        coupons = response.json()
        response.raise_for_status()
        return render(request, 'pet_products/coupon.html', {'coupon_details': coupons})
    except Exception as e:
        messages.error(request, f"Error retrieving coupons: {str(e)}")
        return render(request, 'error.html', {'error': f"Error retrieving coupons: {str(e)}"})

@user_passes_test(lambda u: u.is_staff)
def generate_coupon(request):
    try:
        response = requests.post(COUPON_API, json={'operation': 'create_coupon_code'})
        response.raise_for_status()
        data = response.json()
        print(data)
        messages.success(request, "Coupon generated successfully!")  # Add success message
        return redirect('animal_shelter:index')  # Redirect to home page after generating coupon
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def apply_coupon(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coupon_code = data.get("couponCode")
            if not coupon_code:
                return JsonResponse({"success": False, "message": "Coupon code is required."})
            
            order_total = calculate_order_total(request.user)
            print("Coupon code:", coupon_code)  # Print coupon code
            print("Order total:", order_total)  # Print order total
            
            try:
                response = requests.post(
                    COUPON_API,
                    json={"operation": "validate_coupon","coupon_code": coupon_code, "order_total": order_total},
                    headers={'Content-Type': 'application/json'}
                )
                print("Response:", response.text)  # Print response content
                print("Response:", response.status_code)  # Print response content
                data = response.json()
                if response.status_code == 200:
                    discount = data.get("discount")
                    new_total = data.get("new_total")
                    
                    # Ensure discount and new_total are properly serialized
                    discount = Decimal(discount)
                    new_total = Decimal(new_total)
                    
                    return JsonResponse(
                        {"success": True, "discount": discount, "new_total": new_total},
                        encoder=DecimalEncoder  # Use custom JSON encoder
                    )
                else:
                    return JsonResponse({"success": False, "message": data.get("message")})
            except Exception as e:
                print("Exception:", e)  # Print exception
                return JsonResponse({"success": False, "message": str(e)})
        except Exception as e:
            print("Exception:", e)  # Print exception
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method."})

def calculate_order_total(user):
    cart_items = CartItem.objects.filter(user=user)
    total = sum(float(item.product.price * item.quantity) for item in cart_items)
    return total

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)