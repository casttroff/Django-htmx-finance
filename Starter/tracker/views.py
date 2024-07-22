from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.paginator import Paginator
from tracker.models import Transaction
from tracker.filters import TransactionFilter
from tracker.forms import TransactionForm, ContactForm
from django_htmx.http import retarget

def index(request):
    context = {
        'form': ContactForm()
    }
    return render(request, 'tracker/index.html', context)

@login_required
def transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user)
        .select_related('category', 'user')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1)
    total_income = transaction_filter.qs.get_total_income()
    total_expense = transaction_filter.qs.get_total_expense()
    context = {
        'transactions': transaction_page,
        'filter': transaction_filter, 
        'total_income': total_income, 
        'total_expense': total_expense,
        'net_income': total_income - total_expense
    }

    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)    
    return render(request, 'tracker/transactions-list.html', context)


@login_required
def create_trasaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': "Transacción agregada"}

            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = {'form': TransactionForm()}
    return render(request, 'tracker/partials/create-transaction.html', context)
    

@login_required
def update_trasaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':

        # Pass instance as a paramenter to update object, 
        # anywise a new object will be created.

        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction.save()
            context = {'message': "Transacción actualizada"}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            print("form", form.errors)
            context = {
                'form': form,
                'transaction': transaction
            }
            response = render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction
    }
    return render(request, 'tracker/partials/update-transaction.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {
        'message': f"La transacción de ${transaction.amount} el {transaction.date} fue eliminada"
    }
    return render(request, 'tracker/partials/transaction-success.html', context)


@login_required
def get_transactions(request):
    # import time
    # time.sleep(1)
    page = request.GET.get('page', 1)
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user)
        .select_related('category', 'user')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(page)

    context = {
        'transactions': transaction_page
    }

    return render(
        request,
        'tracker/partials/transactions-container.html#transaction_list', 
        context
    )