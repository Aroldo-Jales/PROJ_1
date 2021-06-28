from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .utils import *

def index(request):

    items = Item.objects.filter(status=True)
    calc_fee(items.filter(status_payment=False))

    if request.method == 'GET':
        word_key = request.GET.get('word-key')

        init_date = request.GET.get('init-date')
        end_date = request.GET.get('end-date')

        init_value = request.GET.get('init-value')
        end_value = request.GET.get('end-value')

        if (word_key):
            items = items.filter(description__contains=word_key)

        if (init_date and end_date):
            if init_date <= end_date:
                items = items.filter(date__range=[init_date, end_date])
            else:
                message_error(request,'date-range')

        else:    
            if (init_date):
                message_error(request,'incomplete-date-2')
            elif (end_date):
                message_error(request,'incomplete-date-1')

        if (init_value and end_value):
            init_value = float(init_value)
            end_value = float(end_value)
            if init_value <= end_value:
                items = items.filter(value__range=[init_value, end_value])
            else:
                message_error(request,'value-range')
        else:    
            if (init_value):
                message_error(request,'incomplete-value-2')
            elif (end_value):
                message_error(request,'incomplete-value-1')
    
    gain = items.filter(type_item='Receita', status_payment=True).aggregate(Sum('value'))
    to_gain = items.filter(type_item='Receita', status_payment=False).aggregate(Sum('value'))
    
    expenses = items.filter(type_item='Despesa', status_payment=True).aggregate(Sum('value'))
    to_pay = items.filter(type_item='Despesa', status_payment=False).aggregate(Sum('value'))
    
    current_balance = items.filter(status_payment=True).aggregate(Sum('value'))
    
    balance = items.aggregate(Sum('value'))
    
    paginator = Paginator(items, 4)
    page = request.GET.get('page')
    items_list = paginator.get_page(page)
    
    data = {'items_list' : items_list, 'balance' : balance, 'gain' : gain, 'to_gain' : to_gain,'expenses' : expenses, 'to_pay' : to_pay, 'current_balance' : current_balance}
    
    return render(request, 'list_transactions.html', data)

def create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.original_value = item.value

            if item.type_item  == 'Despesa' and item.value > 0 or item.type_item  == 'Receita' and item.value < 0:
                item.value = item.value * (-1)
                item.original_value = item.value
                messages.success(request, 'Registro Salvo', extra_tags='safe')
                item.save()
            
                if item.status_payment == True:
                    item.date_payment = item.date
                    item.fees = 0
                    messages.success(request, 'Registro Salvo', extra_tags='safe')
                    item.save()
            else:
                if item.status_payment == True:
                    item.date_payment = item.date
                    item.fees = 0
                    messages.success(request, 'Registro Salvo', extra_tags='safe')
                    item.save()
                else:
                    item.original_value = item.value
                    messages.success(request, 'Registro Salvo', extra_tags='safe')
                    item.save()

            return redirect('/')
    else:
        form = ItemForm()
        form_cat = CategoryForm()
        return render(request, 'create.html', {'form' : ItemForm , 'form_cat' : CategoryForm, 'categories' : categories})

def wallets(request):
    
    wallets = Wallet.objects.all()
    form = WalletForm()
    data = {'wallets' : wallets, 'form' : form}
    
    if request.method == 'POST':
        form = WalletForm(request.POST)

        if form.is_valid():
            wallet = form.save()
            wallet.save()
            return render(request, 'wallets.html', data)
    else:
        return render(request, 'wallets.html', data)

def categories(request):
    
    categories = Category.objects.all()
    form = CategoryForm()
    data = {'categories' : categories, 'form' : form}
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            item = form.save()
            item.save()
            return render(request, 'categories.html', data)
    else:
        return render(request, 'categories.html', data)
        
def update(request, id):
    item = get_object_or_404(Item, pk=id)
    form = ItemFormEdit(instance=item)

    if(request.method == 'POST'):
        form = ItemFormEdit(request.POST, instance=item)

        if (form.is_valid()):
            item = form.save(commit=False)
            item.original_value = item.value
            item.save()
            messages.success(request, 'Registro Alterado!', extra_tags='safe')

            return redirect('/')
        else:
            return render(request, 'update.html', {'form': form, 'item': item})
    else:
        return render(request, 'update.html', {'form': form, 'item': item})

def delete(request, id):
    item = get_object_or_404(Item, pk=id)
    item.status = False
    item.save()
    message_error(request,'delete')
    
    return redirect('/')

def delete_cat(request, id):
    cat = get_object_or_404(Category, pk=id)
    
    categories = Category.objects.all()
    form = CategoryForm()
    data = {'categories' : categories, 'form' : form}

    not_delete = cat.is_deletable()
    
    if not_delete:
        message_error(request, 'not_delete')
        return render(request, 'categories.html', data)
    
    else:
        cat.delete()
        message_error(request, 'delete_cat')
        return render(request, 'categories.html', data)

def trash(request):
    items = Item.objects.filter(status=False)
    data = {'items' : items}
    return render(request, 'trash.html', data)

def permanently_delete(request, id):
    item = get_object_or_404(Item, pk=id)
    item.delete()
    message_error(request,'permanently_delete')

    return redirect('/')

def recycle(request, id):
    item = get_object_or_404(Item, pk=id)

    item.status = True
    item.save()
    messages.success(request, 'Registro recuperado!', extra_tags='safe')

    return redirect('/')

def pay(request, id):
    item = get_object_or_404(Item, pk=id)

    item.status_payment = True
    item.date_payment = item.date
    item.fees = 0
    item.save()

    return redirect('/')

def calc_fee(items):

    for item in items:
        if date.today() > item.date_payment:
            days = days_between_dates(item.date_payment)

            item.value = item.original_value + (item.original_value * ((item.fees/100)*days))
            item.save()

def message_error(request, invalid_type):
    messages_invalid = {
        'date-range': "A data inicial é maior que a final!",
        'incomplete-date-1': "Preencha a data inicial!",
        'incomplete-date-2': "Preencha a data final!",
        'value-range': "O valor inicial é maior que o final!",
        'incomplete-value-1': "Preencha o valor inicial!",
        'incomplete-value-2': "Preencha o valor final!",
        'delete': "Registro movido para a lixeira!",
        'permanently_delete': "Registro removido permanetimente!",
        'date_form': "A data de vencimento é menor que a data inicial",
        'delete_cat': "Categoria removida",
        'not_delete' : "A categoria está ligada a outros registros"
    }
    return messages.error(request, messages_invalid.get(invalid_type))

