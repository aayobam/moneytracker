from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone



class Budget(models.Model):
    """
    The user creates a budget plan for the month or year and adds the amount eg 100,000.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    budget_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


    
class Category(models.Model):
    """
    The user creates new categories that suits his or her budget plan(s).
    """

    name = models.CharField(max_length=100, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    The user creates expenses or incomes to be added or deducted from the budget.
    the budget balance should also be updated after every transactions.
    """

    payment_type = [
        ("Cash", "cash"),
        ("Card", "card"),
    ]

    transactionType = [
        ("Expenses", "expenses"),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, related_name='transactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    payment_type = models.CharField(choices=payment_type, max_length=30)
    transaction_type = models.CharField(choices=transactionType, max_length=50)
    transaction_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("budget_detail", kwargs={"pk":self.pk})
    