from django import forms
from django.forms import ModelForm
from .models import Item, Category, Wallet

class DateInput(forms.DateInput):
    input_type = 'date'

class WalletForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['status','original_value']
        widgets = {
            'date': DateInput(),
            'date_payment': DateInput()
        }

class ItemFormEdit(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['status','status_payment','date_payment','fees','original_value']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'date_input'})
        }   
