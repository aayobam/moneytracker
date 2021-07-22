from django.contrib import admin
from .models import  Budget, Category,Transaction



admin.site.site_title='Budget App Project'
admin.site.site_header = "Budget Administration"

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget_name', 'amount')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','budget','amount', 'category', 'payment_type', 
    'transaction_type', 'description', 'transaction_date', 'updated_at')