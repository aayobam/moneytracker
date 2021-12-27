from budget.forms import TransactionForm, BudgetForm
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Budget,Transaction
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator




# user is able to create one or more budgets 
@login_required(login_url="account-login")
def budget_list_view(request):
    template_name = "budget/budget_list.html"
    budgets = Budget.objects.filter(user=request.user)
    context = {"budgets":budgets}
    return render(request, template_name, context)


# user is able to view details about the budget(s) inlcuding its transaction or expense histories.
@login_required(login_url="account-login")
def budget_detail_view(request, pk):
    user = request.user
    template_name = "budget/budget_detail.html"
    budget = get_object_or_404(Budget, pk=pk)
    transactions = Transaction.objects.filter(user=user, budget=budget)
    paginator = Paginator(transactions, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    budget_balance = 0
    total_expenses = 0
    transaction = 0

    for transaction in transactions:
        total_expenses += transaction.amount
        budget_balance = budget.amount - total_expenses
    context = {
        "budget":budget,
        "transaction":transaction,
        "transactions":transactions,
        "total_expenses":total_expenses,
        "budget_balance":budget_balance,
        "page_obj":page_obj
    }
    return render(request,template_name, context)



# User is able to create budget on the homepage
@login_required(login_url="account-login")
def create_budget(request):
    """"
    User is able to create budget on the homepage
    NOTE: the budget that comes first on the list of budgets created by the user can be used
    """
    template_name = "budget/budget_form.html"
    if request.method == 'POST':
        budget_form = BudgetForm(request.POST)
        if budget_form.is_valid():
            form = budget_form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "Budget Created")
            return redirect("budget_list")
        else:
            return False
    else:
        budget_form = BudgetForm()
    context = {"budget_form":budget_form}
    return render(request, template_name, context)


# user is able to update created budget if there are errors during creation.
def update_budget(request,pk):
    template_name = "budget/budget_form.html"
    budget = get_object_or_404(Budget, pk=pk)
    budget_form = BudgetForm(request.POST, instance=budget)
    if request.method == 'POST':
        if budget_form.is_valid():
            budget_form.save()
            messages.success(request, "Budget Updated")
            return redirect("budget_list")
        else:
            return False
    else:
        budget_form = BudgetForm(instance=budget)
    context = {"budget_form":budget_form}
    return render(request, template_name, context)


# User is able to delete budget(s)
def delete_budget(request,pk):
    budget = get_object_or_404(Budget, pk=pk)
    budget.delete()
    messages.warning(request,f"Budget Deleted")
    return redirect("budget_list")


# User is able to create expense transactions
@login_required(login_url="account-login")
def create_transaction(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    template_name = "budget/transaction_form.html"
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            form = transaction_form.save(commit=False)
            form.user = request.user
            form.budget = budget
            form.save()
            messages.success(request, "Expense Created")
            return redirect("budget_detail", pk)
        else:
            return False
    else:
        transaction_form = TransactionForm()
    context = {"transaction_form":transaction_form, "budget":budget}
    return render(request, template_name, context)


# User is able to delete expense transactions(s)
class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    template_name = "budget/confirm_delete_expense.html"
    model = Transaction
    success_url = reverse_lazy("budget_list")

    def form_valid(self, form):
        messages.success(self.request, f"{Transaction.category.name} Deleted")
        return super().form_valid(form)


# User is able to update expense transaction should in case there is a mistake during creation.
@login_required(login_url="account-login")
def update_expense(request, pk):
    template_name = "budget/update_expense.html"
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction_form = TransactionForm(request.POST, instance=transaction)
    if request.method == 'POST':
        if transaction_form.is_valid():
            transaction_form.save()
            messages.success(request, "Expense Updated")
            return redirect("budget_list")
        messages.error(request, "unable to update expense, please try again")
        return redirect("update_transaction", pk)
    else:
        transaction_form = TransactionForm(instance=transaction)
    context = {"transaction_form":transaction_form, "transaction":transaction}
    return render(request, template_name, context)