from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm

def sign_up(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            messages.success(request,
                'Account has been successfully created for {}!'.format(un))
            return redirect('sign_in')
    elif request.method == "GET":
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        # Redirect to a specific page after sign-out if needed
        return redirect('users:sign_in')  # Assuming you have a 'sign_in' URL name
    # Handle cases where the sign-out URL is accessed via GET method (possibly show an error page)
    # You may choose to handle GET requests differently, like showing a confirmation page or redirecting elsewhere
    return redirect('users:sign_in')  # Redirect to sign-in page by default
