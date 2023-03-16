from django.shortcuts import render
from .models import Customer
from django.shortcuts import redirect
from .forms import LoginForm, CustomerRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def customer_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                password=data['password'],
                username=data['username'],
            )
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home_page')
            else:
                form = LoginForm()
                context = {
                    'login': 'active',
                    'title': 'Login',
                    'form': form
                }
                messages.success(request, "User not found")
                return render(request, 'contact.html', context)
    else:
        form = LoginForm()
        context = {
            'login': 'active',
            'title': 'Login',
            'form': form
        }
        return render(request, 'contact.html', context)


def customer_logout(request):
    logout(request)
    return redirect('home_page')


def customer_register(request):
    form = CustomerRegistrationForm()
    context = {
        'signup': 'active',
        'title': 'Registration',
        'form': form
    }
    if request.method == 'POST':
        customer_form = CustomerRegistrationForm(request.POST)
        if customer_form.is_valid():
            if customer_form.cleaned_data['password'] == customer_form.cleaned_data['password_2'] and len(customer_form.cleaned_data['password']) >= 5:
                new_customer = customer_form.save(commit=False)
                new_customer.set_password(
                    customer_form.cleaned_data['password']
                )
                new_customer.save()
                form_login = LoginForm()
                context_login = {
                    'login': 'active',
                    'title': 'Login',
                    'form': form_login
                }
                return render(request, 'contact.html', context_login)
            else:
                messages.success(request, "Your password must be at least 5 characters long")
                return render(request, 'contact.html', context)
        else:
            messages.success(request, "The user is already registered or the passwords you entered are not the same")
            return render(request, 'contact.html', context)
    else:
        return render(request, 'contact.html', context)


def customer_edit(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.user.id)
        customer.username = request.POST['customer_name']
        customer.email = request.POST['customer_email']
        customer.phone_number = request.POST['customer_phone']
        customer.save()
        return redirect('home_page')
    else:
        context = {
            'change_profile': 'active',
            'title': 'About Customer',
            'customer_name': request.user.username,
            'customer_email': request.user.email,
            'customer_phone': request.user.phone_number,
        }
        return render(request, 'contact.html', context)
