from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
=======
class Wallet(models.Model):
    name = models.CharField('Nome Carteira', max_length=100)
    def __str__(self):
        return self.name

>>>>>>> cf4e4c6 (wallet)
class Category(models.Model):
    name = models.CharField('Nome categoria', max_length=100)
    def __str__(self):
        return self.name

<<<<<<< HEAD
=======
    def is_deletable(self):
        related_list = []
        for relation in self._meta.get_fields():
            try:
                related = relation.related_model.objects.filter(**{relation.field.name: self})
                if related.exists():
                    related_list.append(related)
            except: 
                pass
        return related_list

>>>>>>> cf4e4c6 (wallet)
class Item(models.Model):
    
    description = models.CharField('Descrição', max_length=100)
    value = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    original_value = models.DecimalField('Valor original', max_digits=8, decimal_places=2, blank=True)

    CHOICE_TYPE = (
        ('Receita', 'Receita'),
        ('Despesa', 'Despesa')
    )
    
    type_item = models.CharField('Tipo', max_length=50, choices=CHOICE_TYPE)

    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField('Data')

    status_payment = models.BooleanField('Pago', default=True) 
    date_payment = models.DateField('Data Vencimento', blank=True)
    fees = models.DecimalField('Juros', max_digits=5, decimal_places=1, blank=True)

    status = models.BooleanField(default=True) # 
    
    def __str__(self):
        return self.description