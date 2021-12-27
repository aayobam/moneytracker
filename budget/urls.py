from django.urls import path
from .views import *


urlpatterns = [
    path('home/budget', budget_list_view, name="budget_list"),
    path('dashboard/budget/<int:pk>', budget_detail_view, name="budget_detail"),
    path('create-budget/', create_budget, name="create_budget"),
    path('update-budget/<int:pk>', update_budget, name="update_budget"),
    path('delete-budget/<int:pk>', delete_budget, name="delete_budget"),

    path('create-transaction/<int:pk>',create_transaction, name="create_transaction"),
    path('delete-expense/<int:pk>', DeleteTransactionView.as_view(), name="delete_transaction"),
    path('update-expense/<int:pk>', update_expense, name="update_transaction"),
]
