from django.contrib import admin
from .models import Item, Category, Wallet

admin.site.register(Wallet)
admin.site.register(Item)
admin.site.register(Category)
