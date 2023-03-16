from django.contrib import admin
from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Customer
from django.contrib.auth.admin import UserAdmin


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ['id', 'username', 'email', 'phone_number']
    list_display_links = ['username']


admin.site.register(Customer, CustomerAdmin)
