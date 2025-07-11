from django.conf import settings
from django.db import models

from shop.models import Product


class Order(models.Model):
    """
    Модель заказа
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Заказ {self.id}, {self.first_name} {self.last_name}'

    def get_total_cost(self):
        """
        Стоимость заказа
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_stripe_url(self):
        """
        Получение URL Stripe
        """
        if not self.stripe_id:
            # никаких ассоциированных платежей
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # путь Stripe для тестовых платежей
            path = '/test/'
        else:
            # путь Stripe для настоящих платежей
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    """
    Модель товаров в заказе
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """
        Стоимость товара(-ов) в заказе
        """
        return self.price * self.quantity
