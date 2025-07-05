from io import BytesIO
from pathlib import Path

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по эл. почте при успешной оплате заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Инструменты - Счёт-фактура №{order.id}'
    message = 'Пожалуйста, ознакомьтесь с приложенной счёт-фактурой за Вашу недавнюю покупку.'
    email = EmailMessage(
        subject, message, 'admin@web.top', [order.email]
    )
    # сгенерировать PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(Path(settings.STATIC_ROOT) / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(
        out, stylesheets=stylesheets
    )
    # прикрепить PDF-файл
    email.attach(
        f'Заказ {order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )
    # отправить электронное письмо
    email.send()
