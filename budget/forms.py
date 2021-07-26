from django import forms
from django.contrib.auth.models import User
from .models import Transaction, Budget




class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['budget', 'category', 'amount', 'transaction_type', 'payment_type', 'description']

class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ['budget_name', "amount"]