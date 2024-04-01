from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login  # Updated import
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserSignUpForm

def sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            messages.success(request,
                'Account has been successfully created for {}!'.format(un))
            return redirect('users:sign_in')  # Redirect to sign-in page after sign-up
    elif request.method == "GET":
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('users:sign_out_page')  # Redirect to the sign-out page after sign-out
    return redirect('users:sign_in')  # Redirect to sign-in page by default

def sign_out_page(request):
    return render(request, 'users/sign_out.html')  # Render the sign-out page template

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # Redirect to the home page after successful login
        else:
            # Handle invalid login
            return render(request, 'users/sign_in.html', {'error_message': 'Invalid username or password'})

    return render(request, 'users/sign_in.html')
