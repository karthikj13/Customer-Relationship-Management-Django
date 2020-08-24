from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crm.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
