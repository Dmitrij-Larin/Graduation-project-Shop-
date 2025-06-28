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
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_url(reverse('payment:canceled'))
        cancel_url = request.build_absolute_url(reverse('payment:canceled'))
        # данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # создать сеанс оформления платежа Stripe
        session= stripe.checkout.Session.create(**session_data)
        # перенаправить к платёжной форме Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
