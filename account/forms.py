from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number']


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password_2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Reset password"
    )

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number']

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError(
                "Passwords must match"
            )
        return data['password_2']
