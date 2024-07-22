import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Transaction, Category


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        # create categories

        categories = [
            "Gastos médicos",
            "Salud y bienestar",
            "Alimentación",
            "Educación",
            "Trabajo",
            "Transporte",
            "Entretenimiento",
            "Viajes",
            "Tecnología",
            "Inversiones",
            "Seguros",
            "Gastos personales",
            "Mascotas",
            "Hogar y servicios",
            "Impuestos",
            "Cultura"
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        # get the user

        user = User.objects.filter(username='fdv').first()

        if not user:
            user = User.objects.create_superuser(
                username='fdv',
                password='test'
            )

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]

        for i in range(32):
            Transaction.objects.create(
                category=random.choice(categories),
                user=user,
                amount=random.uniform(1, 2500),
                date=fake.date_between(start_date='-1y'),
                type=random.choice(types)
            )
