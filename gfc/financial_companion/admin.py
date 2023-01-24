"""Configuration of the admin interface of financial_companion."""

from django.contrib import admin
from .models import  (
    User, 
    Category, 
    Account, PotAccount, BankAccount, 
    Transaction, 
    CategoryTarget, AccountTarget, UserTarget
)

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_staff', 'profile_picture'
    ]

@admin.register(Category)
class Category(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'id', 'name', 'description'
    ]

@admin.register(Account)
class Account(admin.ModelAdmin):
    """Configuration of the admin interface for account."""

    list_display = [
        'id', 'name', 'description'
    ]

@admin.register(PotAccount)
class PotAccount(admin.ModelAdmin):
    """Configuration of the admin interface for pot account."""

    list_display = [
        'id', 'name', 'description', 'user_id', 'balance', 'currency'
    ]

@admin.register(BankAccount)
class BankAccount(admin.ModelAdmin):
    """Configuration of the admin interface for bank account."""

    list_display = [
        'id', 'name', 'description', 'user_id', 'balance', 'currency',
        'bank_name', 'account_number', 'sort_code', 'iban', 'interest_rate'

@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'amount', 'currency', 'sender_account', 'receiver_account', 'category', 'description'
    ]

@admin.register(CategoryTarget)
class CategoryTarget(admin.ModelAdmin):
    list_display = [
        'transaction_type', 'timespan', 'amount', 'currency', 'category_id'
    ]

@admin.register(UserTarget)
class UserTarget(admin.ModelAdmin):
    list_display = [
        'transaction_type', 'timespan', 'amount', 'currency', 'user_id'
    ]

@admin.register(AccountTarget)
class AccountTarget(admin.ModelAdmin):
    list_display = [
        'transaction_type', 'timespan', 'amount', 'currency', 'account_id'
    ]