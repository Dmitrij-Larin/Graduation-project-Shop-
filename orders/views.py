import os
import weasyprint
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from orders.tasks import order_created


def order_create(request):
    cart = Cart(request)
    # Проверка на аутентификацию пользователя
    if not request.user.is_authenticated:
        return redirect('user_login')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            # Создание заказа и связывание с пользователем
            order = form.save(commit=False)
            order.user = request.user  # Связываем заказ с пользователем
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Очистка корзины после создания заказа
            cart.clear()

            # Запуск асинхронного задания
            order_created.delay(order.id)

            # Сохранение ID заказа в сессию
            request.session['order_id'] = order.id

            # Перенаправление на страницу платежа
            return redirect(reverse('payment:process'))

    else:
        # Если метод GET, создаем пустую форму
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (f'filename=order_{order.id}.pdf')
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(
                os.path.join(settings.STATIC_ROOT, 'css/pdf.css')
            )
        ]
    )
    return response
