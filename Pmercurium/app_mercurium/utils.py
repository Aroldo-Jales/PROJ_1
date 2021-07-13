from datetime import date
from django.contrib import messages
from django.db.models import Sum
from .models import *

def days_between_dates(date):
    today = date.today()
    return abs((today-date).days)

def filter_items(request, items, word_key=None, init_date=None, end_date=None, init_value=None, end_value=None):

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
    return items    

def modify_item(item):

    if item.type_item  == 'Despesa' and item.value > 0 or item.type_item  == 'Receita' and item.value < 0:
        item.value = item.value * (-1)

    if item.status_payment == True:
        item.date_payment = item.date
        item.fees = 0
    
    item.original_value = item.value
    return item

def over_limit(request, item, wallet):   

    if wallet.limit == 0:
        return False
    else:
        items_list = Item.objects.filter(wallet__pk=wallet.id, status=True, type_item='Despesa')
        value_left = 0
        for items in items_list:
            value_left += items.value

        if value_left == 0:
            if item.value < wallet.limit:
                return True
            else:
                return False
        else:
            total_left = value_left + item.value
            if total_left < wallet.limit:
                return True
            else:
                return False

def verify_item(request, item, type_=''):
    if type_ == 'create':
        wallet = item.wallet
        items = Item.objects.filter(wallet__pk=wallet.id)
        if items.filter(description__iexact=item.description):
            message_error(request, 'invalid_name')
            return True
        else:
            return False
    else:
        wallet = item.wallet
        items = Item.objects.filter(wallet__pk=wallet.id)
        if items.filter(description__iexact=item.description).exclude(pk=item.id):
            message_error(request, 'invalid_name')
            return True
        else:
            return False

def wallet_limit_is_valid(request, wallet):
    max_value = Item.objects.filter(wallet__pk=wallet.id).order_by('value')[0]
    if max_value.status == False:
        message_error(request, 'invalid_limit_trash', max_value.description)
        return True
    elif max_value.status == True:
        message_error(request, 'invalid_limit', max_value.description)
        return True
    else:
        return False
    
def message_error(request, invalid_type, name=''):
    messages_invalid = {
        'invalid_limit': f"Limite inválido, pois é mais baixo que do registro {name}.",
        'invalid_limit_trash': f"Limite inválido, pois é mais baixo que do registro {name} na lixeira.",
        'invalid_name': "Este nome já está sendo utilizado em outro registro.",
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