import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
from payment.tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe веб-перехватчик
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        # Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Недопустимая подпись
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if (
                session.mode == 'payment' and session.payment_status == 'paid'
        ):
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # Пометить заказ как оплаченный
            order.paid = True
            # сохранить id платежа Stripe
            order.stripe_id = session.payment_intent
            order.save()
            # запустить асинхронное задание
            payment_completed.delay(order.id)

    return HttpResponse(status=200)
