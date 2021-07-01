from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('wallets.html', wallets),
    path('create.html', create),
    path('update/<int:id>', update),
    path('trash.html', trash),
    path('delete/<int:id>', delete),
    path('permanentlydelete/<int:id>', permanently_delete),
    path('recycle/<int:id>', recycle),
    path('pay/<int:id>', pay),

    path('categories.html', categories),
    path('delete_cat/<int:id>', delete_cat)
]
