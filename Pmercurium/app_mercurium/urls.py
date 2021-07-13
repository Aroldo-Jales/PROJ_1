from django.urls import path
from .views import *

urlpatterns = [
    path('', wallets),
    path('wallet_transactions/<int:id>', wallet_transactions),
    path('confirm_delete_wallet/<int:id>', confirm_delete_wallet),
    path('update_wallet/<int:id>', update_wallet),
    path('delete_wallet/<int:id>', delete_wallet),

    path('create/<int:id>', create),
    path('update/<int:id>', update),
    path('pay/<int:id>', pay),

    path('categories/<int:id>', categories),
    path('update_cat/<int:id>', update_cat),
    path('delete_cat/<int:id>', delete_cat),

    path('trash/<int:id>', trash),
    path('delete/<int:id>', delete),
    path('permanentlydelete/<int:id>', permanently_delete),
    path('recycle/<int:id>', recycle),

]
