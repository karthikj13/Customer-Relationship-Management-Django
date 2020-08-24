from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import *
from .forms import OrderForm
from .filters import OrderFilter
from .decorators import allowed_users,admin_only

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers,'total_orders':total_orders,
                'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'crm/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    paginator = Paginator(products,4)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:         #If page is not an integer deliver the first page
        product = paginator.page(1)     
    except EmptyPage:            #if page is out of range deliver last page of results
        product = paginator.page(paginator.num_pages)

    return render(request,'crm/products.html',{'page':page,'product':product})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'total_orders':total_orders,
            'order_delivered':order_delivered,'order_pending':order_pending}

    return render(request, 'crm/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders,
             'total_orders':total_orders,'myFilter':myFilter}
    return render(request,'crm/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=4)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset,'customer':customer}
    return render(request, 'crm/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'crm/update_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    return render(request, 'crm/delete_order.html', {'order':order})