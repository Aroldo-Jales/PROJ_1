from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .utils import *

@login_required
def wallets(request):
    wallets = Wallet.objects.filter(user=request.user)
    data = {'wallets' : wallets}

    if request.method == 'POST':
        form = WalletForm(request.POST)

        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            if wallet.limit > 0:
                wallet.limit = wallet.limit * (-1)

            wallet.save()
            message_sucess(request, 'save', wallet.name)
            return redirect('/')
    else:
        return render(request, 'wallets.html', data)

def update_wallet(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    form = WalletForm(instance=wallet)

    if wallet.user == request.user:
        if request.method == 'POST':
            form = WalletForm(request.POST, instance=wallet)

            if form.is_valid():
                wallet = form.save(commit=False)
                wallet.user = request.user
                if wallet.limit > 0:
                    wallet.limit = wallet.limit * (-1)

                wallet.save()
                message_sucess(request, 'save', wallet.name)
                return redirect('/')
            else:
                return redirect('/')
        else:
            return render(request, 'confirm/edit_wallet.html', {'form' : form, 'wallet' : wallet})
    else:
        raise PermissionDenied()
    
def confirm_delete_wallet(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    data = {'wallet' : wallet}
    
    if wallet.user == request.user:
        return render(request, 'confirm/confirm_delete_wallet.html', data)
    else:
        raise PermissionDenied()

def delete_wallet(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    if wallet.user == request.user:
        wallet.delete()
        message_error(request, 'delete_wallet', wallet.name)
        return redirect('/')
    else:
        raise PermissionDenied()


@login_required
def wallet_transactions(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    if wallet.user == request.user:
        items = Item.objects.filter(wallet__pk=id, status=True)
        category = Category.objects.filter(wallet__pk=id)
        items = items.order_by('date_payment')

        calc_fee(items.filter(status_payment=False))

        if request.method == 'GET':
            word_key = request.GET.get('word-key')

            init_date = request.GET.get('init-date')
            end_date = request.GET.get('end-date')      

            init_value = request.GET.get('init-value')
            end_value = request.GET.get('end-value')

            items = filter_items(request, items, word_key, init_date, end_date, init_value, end_value)
            
        gain = items.filter(type_item='Receita', status_payment=True).aggregate(Sum('value'))
        to_gain = items.filter(type_item='Receita', status_payment=False).aggregate(Sum('value'))
        expenses = items.filter(type_item='Despesa', status_payment=True).aggregate(Sum('value'))
        to_pay = items.filter(type_item='Despesa', status_payment=False).aggregate(Sum('value'))
        current_balance = items.filter(status_payment=True).aggregate(Sum('value'))
        balance = items.aggregate(Sum('value'))

        paginator = Paginator(items, 8)
        page = request.GET.get('page')
        items_list = paginator.get_page(page)

        data = {
        'items_list' : items_list, 
        'balance' : balance, 
        'gain' : gain, 
        'to_gain' : to_gain,
        'expenses' : expenses, 
        'to_pay' : to_pay, 
        'current_balance' : current_balance,
        'wallet' : wallet,
        'category' : category
        }
        return render(request, 'wallet_transactions.html', data)
    else:
        raise PermissionDenied()

@login_required
def create(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    categories = Category.objects.filter(wallet__pk=id)
    if wallet.user == request.user:
        if request.method == 'POST':
            form = ItemForm(request.POST)

            if form.is_valid():
                item = form.save(commit=False)
                item.wallet = Wallet.objects.get(pk=id)
                item = modify_item(item)
                item.original_value = item.value
                wallet = get_object_or_404(Wallet, pk=id)
                if over_limit(request,item, wallet):
                    message_error(request, 'over_limit', item.description)
                    return redirect(f'/wallet_transactions/{wallet.id}')
                else:
                    item.save()
                    message_sucess(request, 'save', item.description)
                    return redirect(f'/wallet_transactions/{wallet.id}')
            else:
                return redirect(f'/wallet_transactions/{wallet.id}')
        else:
            form = ItemForm()
            form_cat = CategoryForm()
            return render(request, 'create.html', {'wallet' : wallet, 'categories' : categories})
    else:
        raise PermissionDenied()
@login_required
def update(request, id):
    item = get_object_or_404(Item, pk=id)
    wallet = item.wallet
    if wallet.user == request.user:
        form = ItemFormEdit(instance=item)

        if(request.method == 'POST'):
            form = ItemFormEdit(request.POST, instance=item)

            if (form.is_valid()):
                item = form.save(commit=False)
                item.wallet = Wallet.objects.get(pk=id)
                item = modify_item(item)
                item.original_value = item.value
                wallet = get_object_or_404(Wallet, pk=id)
                if over_limit(request,item, wallet):
                    message_error(request, 'over_limit', item.description)
                    return redirect(f'/wallet_transactions/{id}')
                else:
                    item.save()
                    message_sucess(request, 'save', item.description)
                    return redirect(f'/wallet_transactions/{id}')
            else:
                return render(request, 'update.html', {'form': form, 'item': item})
        else:
            return render(request, 'update.html', {'form': form, 'item': item})
    else:
        raise PermissionDenied()

@login_required
def delete(request, id):
    item = get_object_or_404(Item, pk=id)
    wallet = item.wallet
    if wallet.user == request.user:
        item.status = False
        item.save()
        message_error(request,'delete')

        return redirect(f'/wallet_transactions/{wallet.id}')
    else:
        raise PermissionDenied()

@login_required
def categories(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    if wallet.user == request.user:
        categories = Category.objects.filter(wallet__pk=id)
        form = CategoryForm()
        data = {'categories' : categories, 'form' : form, 'wallet' : wallet}
        
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            
            if form.is_valid():
                cat = form.save(commit=False)
                cat.wallet = wallet
                cat.save()
                return redirect(f'/wallet_transactions/{wallet.id}')
        else:
            return render(request, 'categories.html', data)
    else:
        raise PermissionDenied()

@login_required
def update_cat(request, id):
    cat = get_object_or_404(Category, pk=id)
    wallet = cat.wallet
    if wallet.user == request.user:
        categories = Category.objects.filter(wallet__pk=id)
        
        form = CategoryForm(instance=cat)
        data = {'categories' : categories, 'form' : form, 'wallet' : wallet}
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=cat)
            if form.is_valid():
                cat = form.save(commit=False)
                cat.wallet = wallet 
                cat.save()
                message_sucess(request, 'edit_cat', cat.name)
                return redirect(f'/wallet_transactions/{wallet.id}')
        else:
            return render(request, 'categories.html', data)    
    else:
        raise PermissionDenied()

@login_required
def delete_cat(request, id):
    cat = get_object_or_404(Category, pk=id)
    wallet = cat.wallet
    if wallet.user == request.user:

        categories = Category.objects.all()
        form = CategoryForm()
        data = {'categories' : categories, 'form' : form}

        cat.delete()
        message_error(request, 'delete_cat')
        return redirect(f'/wallet_transactions/{wallet.id}')

    else:
        raise PermissionDenied()


@login_required
def trash(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    if wallet.user == request.user:
        items = Item.objects.filter(wallet__pk=id, status=False)

        if request.method == 'GET':
            word_key = request.GET.get('word-key')

            init_date = request.GET.get('init-date')
            end_date = request.GET.get('end-date')      

            init_value = request.GET.get('init-value')
            end_value = request.GET.get('end-value')

            items = filter_items(request, items, word_key, init_date, end_date, init_value, end_value)

        data = {'items' : items , 'wallet' : wallet}
        return render(request, 'trash.html', data)
    else:
        raise PermissionDenied()

@login_required
def permanently_delete(request, id):
    item = get_object_or_404(Item, pk=id)
    wallet = item.wallet
    if wallet.user == request.user:
        item.delete()
        message_error(request, 'permanently_delete', item.description)
        return redirect(f'/wallet_transactions/{wallet.id}')
    else:
        raise PermissionDenied()

@login_required
def recycle(request, id):
    item = get_object_or_404(Item, pk=id)
    wallet = item.wallet
    if wallet.user == request.user:
        item.status = True
        item.save()
        message_sucess(request, 'recycle', item.description)
        return redirect(f'/wallet_transactions/{wallet.id}')
    else:
        raise PermissionDenied()

@login_required
def pay(request, id):
    item = get_object_or_404(Item, pk=id)
    wallet = item.wallet
    if wallet.user == request.user:
        item.status_payment = True
        item.date_payment = item.date
        item.fees = 0
        item.save()
        return redirect(f'/wallet_transactions/{wallet.id}')
    else:
        raise PermissionDenied()

def calc_fee(items):

    for item in items:
        if date.today() > item.date_payment:
            days = days_between_dates(item.date_payment)

            item.value = item.original_value + (item.original_value * ((item.fees/100)*days))
            item.save()

def message_sucess(request, sucess_type, name=''):
    messages_sucess = {
        'save': f"Registro {name} salvo!",
        'recycle' : f"Registro {name} recuperado!",
        'edit' : f"Registro {name} alterado!",
        'edit_cat' : f"Categoria {name} alterada!"
    }

    return messages.success(request, messages_sucess.get(sucess_type), extra_tags='safe')

def message_error(request, invalid_type, name=''):
    messages_invalid = {
        'delete_cat': f"A categoria {name} foi removida.",
        'delete_wallet': f"A carteira {name} foi removida.",
        'over_limit': f"O registro {name} passa do valor limite da carteira.",
        'related_list': f"{name}",
        'date-range': "A data inicial é maior que a final!",
        'incomplete-date-1': "Preencha a data inicial!",
        'incomplete-date-2': "Preencha a data final!",
        'value-range': "O valor inicial é maior que o final!",
        'incomplete-value-1': "Preencha o valor inicial!",
        'incomplete-value-2': "Preencha o valor final!",
        'delete': f"Registro {name} movido para a lixeira!",
        'permanently_delete': f"Registro {name} removido permanetimente!",
        'date_form': "A data de vencimento é menor que a data inicial",
        'delete_cat': f"Categoria {name} removida",
        'not_delete' : f"A categoria {name} está ligada a outros registros"
    }

    return messages.error(request, messages_invalid.get(invalid_type))
