import pytest
from tracker.models import Transaction

@pytest.mark.django_db
def test_queryset_get_incomes_method(transactions):
    qs = Transaction.objects.get_incomes()
    assert qs.count() > 0
    assert all(
        transaction.type=='ingreso' for transaction in qs
    )

@pytest.mark.django_db
def test_queryset_get_expenses_method(transactions):
    qs = Transaction.objects.get_expenses()
    assert qs.count() > 0
    assert all(
        transaction.type=='gasto' for transaction in qs
    )

@pytest.mark.django_db
def test_queryset_get_total_incomes_method(transactions):
    total_income = Transaction.objects.get_total_income()
    assert total_income == sum(t.amount for t in transactions if t.type=='ingreso')

@pytest.mark.django_db
def test_queryset_get_total_expenses_method(transactions):
    total_expense = Transaction.objects.get_total_expense()
    assert total_expense == sum(t.amount for t in transactions if t.type=='gasto')