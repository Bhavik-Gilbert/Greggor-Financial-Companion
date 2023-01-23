from django import forms
from financial_companion.forms import AddTransactionForm
from financial_companion.models import Transaction
from .test_form_base import FormTestCase
from django.test import TestCase

class AddTransactionFormTestCase(FormTestCase):
    """Test of the add transaction form"""
