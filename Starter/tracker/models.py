from django.db import models
from django.contrib.auth.models import User
from .managers import TransactionQuerySet
from modeltranslation.translator import translator, TranslationOptions



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    objects = TransactionQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'Transacciones'
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} de {self.amount} el {self.date} por {self.user}"


class Product(models.Model):
    class ProductTypes(models.TextChoices):
        ELECTRONIC = 'Electrónico'
        CLOTHING = 'Ropa'
        FOOD = 'Comida'
        BOOK = 'Libro'
        INTERIOR_CLOTHING = 'Ropa interior'
        FURNITURE = 'Mueble'
        ACCESS = 'Accesorio'

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    product_type = models.CharField(max_length=20, choices=ProductTypes.choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} {self.name}"


class LogisticsAgent(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClientAddress(models.Model):
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.ManyToManyField(ClientAddress)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    class OrderChoices(models.TextChoices):
        PENDING = 'Pendiente'
        COMPLETED = 'Completado'
        CANCELLED = 'Cancelado'
        SHIPPED = 'Enviado'
        DELIVERED = 'Entregado'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    logistic_agent = models.ForeignKey(LogisticsAgent, on_delete=models.CASCADE)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=10, choices=OrderChoices.choices, default=OrderChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_products(self):
        return ", ".join([f"{product.category} {product.name}" for product in self.products.all()])

    def __str__(self):
        return f"Orden {self.id} de {self.user.username}"
    
class OrderTranslationOptions(TranslationOptions):
    fields = ('order_status',)