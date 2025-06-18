from django import forms
from orders.models import Order
from django.utils.translation import gettext as _


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city'
        ]

        labels = {
            'first_name': _("Имя"),
            'last_name': _("Фамилия"),
            'email': _("Эл. почта"),
            'address': _("Почтовый адрес"),
            'postal_code': _("Почтовый индекс"),
            'city': _("Город"),
        }
