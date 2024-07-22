import pytest
import random
from django.urls import reverse
from datetime import datetime, timedelta
from tracker.models import Category, Transaction
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_total_values_apper_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # Check totals
    income_total = sum(t.amount for t in user_transactions if t.type == 'ingreso')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'gasto')
    net_income = income_total - expense_total

    response = client.get(reverse('transactions-list'))
    assert response.context['total_income'] == income_total
    assert response.context['total_expense'] == expense_total
    assert response.context['net_income'] == net_income


@pytest.mark.django_db
def test_transaction_type_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # Check types of transactions (Transaction model)
    GET_params = {'transaction_type': 'ingreso'}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'ingreso'

    GET_params = {'transaction_type': 'gasto'}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'gasto'


@pytest.mark.django_db
def test_start_end_date_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # Get transactions from start date
    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date >= start_date_cutoff

    # Get transactions until end date
    end_date_cutoff = datetime.now().date() - timedelta(days=55)
    GET_params = {'end_date': end_date_cutoff}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date <= end_date_cutoff


@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # Get first 2 categories
    category_pks = Category.objects.all()[:2].values_list('pk', flat=True)
    GET_params = {'category': category_pks}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.category.pk in category_pks


@pytest.mark.django_db
def test_add_transaction_request(user, transaction_dict_params, client):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    # Send transaction data

    headers = {'HTTP_HX-Request': 'true'}
    response = client.post(
        reverse('create-transaction'),
        transaction_dict_params,
        **headers
    )
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/partials/transaction-success.html')
    assert Transaction.objects.filter(user=user).count() == user_transaction_count + 1
    

@pytest.mark.django_db
def test_can_not_add_negative_amount_request(user, transaction_dict_params, client):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    # Send transaction data
    transaction_dict_params['amount'] = -55
    response = client.post(
        reverse('create-transaction'),
        transaction_dict_params,
    )
    form = response.context.get('form')
    assert response.status_code == 200
    assert form is not None
    assert form.errors is not None
    assertTemplateUsed(response, 'tracker/partials/create-transaction.html')
    assert Transaction.objects.filter(user=user).count() == user_transaction_count
    assert 'HX-Retarget' in response.headers


@pytest.mark.django_db
def test_update_transaction_request(user, categories, transaction_dict_params, client):
    client.force_login(user)
    assert Transaction.objects.filter(user=user).count() == 1

    transaction = Transaction.objects.first()
    categories = [x.pk for x in categories if x.pk != transaction.category.pk]
    assert len(categories) > 0
    
    new_category_pk = random.choice(categories)
    now = datetime.now().date()
    transaction_dict_params['amount'] = 420
    transaction_dict_params['description'] = 'New description'
    transaction_dict_params['category'] = new_category_pk
    transaction_dict_params['date'] = now

    response = client.post(
        reverse('update-transaction', kwargs={'pk': transaction.pk}),
        transaction_dict_params,
    )

    assert response.status_code == 200
    assert Transaction.objects.filter(user=user).count() == 1
    transaction = Transaction.objects.first()
    assert transaction.amount == 420
    assert transaction.description == 'New description'
    assert transaction.category.id == new_category_pk
    assert transaction.date == now


@pytest.mark.django_db
def test_delete_transaction_request(user, transaction_dict_params, client):
    client.force_login(user)
    assert Transaction.objects.filter(user=user).count() == 1
    transaction = Transaction.objects.first()

    # Send DELETE request
    client.delete(
        reverse('delete-transaction', kwargs={'pk': transaction.pk})
    )

    assert Transaction.objects.filter(user=user).count() == 0