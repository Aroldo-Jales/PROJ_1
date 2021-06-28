from django.contrib import admin
<<<<<<< HEAD
from .models import Item, Category

=======
from .models import Item, Category, Wallet

admin.site.register(Wallet)
>>>>>>> cf4e4c6 (wallet)
admin.site.register(Item)
admin.site.register(Category)