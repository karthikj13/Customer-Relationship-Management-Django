from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, CustomerForm
from crm.models import Customer
from crm.decorators import allowed_users

def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')

    context = {'form':form}
    return render(request, 'users/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}

    return render(request, 'users/account_settings.html', context)
