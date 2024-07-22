from django.db import models

class TransactionQuerySet(models.QuerySet):
    def get_expenses(self):
        return self.filter(type='gasto')
    
    def get_incomes(self):
        return self.filter(type='ingreso')
    
    def get_total_expense(self):
        return self.get_expenses().aggregate(
            total=models.Sum('amount')
            )['total'] or 0
    
    def get_total_income(self):
        return self.get_incomes().aggregate(
            total=models.Sum('amount')
            )['total'] or 0
    
