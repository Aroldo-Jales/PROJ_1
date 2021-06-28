from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
<<<<<<< HEAD
=======
    path('wallets.html', wallets),

>>>>>>> cf4e4c6 (wallet)
    path('create.html', create),
    path('update/<int:id>', update),
    path('delete/<int:id>', delete),
    path('trash.html', trash),
    path('permanentlydelete/<int:id>', permanently_delete),
    path('recycle/<int:id>', recycle),
    path('pay/<int:id>', pay),

    path('categories.html', categories),
    path('delete_cat/<int:id>', delete_cat)
]