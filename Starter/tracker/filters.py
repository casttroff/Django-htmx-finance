import django_filters
from tracker.models import Transaction, Category
from django import forms

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name='type',
        lookup_expr='iexact',
        empty_label='Todos'
    )

    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Fecha desde',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Fecha hasta',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    category= django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type', 'start_date', 'end_date')


    