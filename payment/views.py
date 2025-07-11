from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orders.models import Order

# создать экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    """
    Реализация процесса оплаты через Stripe
    """
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # добавить товарные позиции заказа в сеанс оформления платежа Stripe
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'rub',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )
        # создать сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        # перенаправить к платёжной форме Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    """
    Уведомление об успешной оплате
    """
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    """
    Уведомление об отмене оплаты
    """
    return render(request, 'payment/canceled.html')
