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