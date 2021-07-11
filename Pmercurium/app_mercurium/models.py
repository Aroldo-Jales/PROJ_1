from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField('Nome Carteira', max_length=100)    
    limit = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.name

    def transactions_value(self):
        items_list = Item.objects.filter(wallet__pk=self.id)
        items_list = items_list.filter(status=True)
        total = 0
        for item in items_list:
            total += item.value
            
        return total

    def transactions(self):
        items_list = Item.objects.filter(wallet__pk=self.id)
        items_list = items_list.filter(status=True)
        return len(items_list)
    
    def is_deletable(self):
        items_list = Item.objects.filter(wallet__pk=self.id)
        return len(items_list)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    name = models.CharField('Nome categoria', max_length=100)
    
    def __str__(self):
        return self.name

        # def is_deletable(self):
    #     related_list = []
    #     for relation in self._meta.get_fields():
    #         try:
    #             related = relation.related_model.objects.filter(**{relation.field.name: self})
    #             if related.exists():
    #                 related_list.append(related)
    #         except: 
    #             pass
    #     return related_list

    def is_deletable(self):
        items_list = Item.objects.filter(category__pk=self.id)
        return len(items_list)

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    description = models.CharField('Descrição', max_length=100)
    value = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    original_value = models.DecimalField('Valor original', max_digits=8, decimal_places=2, blank=True)

    CHOICE_TYPE = (
        ('Receita', 'Receita'),
        ('Despesa', 'Despesa')
    )
    
    type_item = models.CharField('Tipo', max_length=50, choices=CHOICE_TYPE)

    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    date = models.DateField('Data')

    status_payment = models.BooleanField('Pago', default=True) 
    date_payment = models.DateField('Data Vencimento', blank=True)
    fees = models.DecimalField('Juros', max_digits=5, decimal_places=1, blank=True)

    status = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.description
