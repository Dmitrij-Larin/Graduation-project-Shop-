import random
import string

from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_new_password, send_register_email
from orders.models import Order


class UserRegisterView(CreateView):
    """
    Представление интерфейса регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def form_valid(self, form):
        """
        Валидация формы при регистрации пользователя
        """
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Представление интерфейса ввода данных для входа в аккаунт
    """
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт'
    }


class UserProfileView(UpdateView):
    """
    Представление профиля пользователя
    """
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'
    extra_context = {
        'title': 'Ваш профиль'
    }

    def get_object(self, queryset=None):
        """
        Проверка соответствия пользователя
        """
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Представление интерфейса для обновления профиля пользователя
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Обновить профиль'
    }

    def get_object(self, queryset=None):
        """
        Представление интерфейса для проверки соответствия пользователя
        """
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """
    Представление интерфейса для изменения пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Изменение пароля'
    }


class UserLogoutView(LogoutView):
    """
    Представление интерфейса для выхода из аккаунта
    """
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта'
    }


class UserDetailView(DetailView):
    """
    Представление информации профиля пользователя
    """
    model = User
    template_name = 'users/user_detail_view.html'

    def get_context_data(self, **kwargs):
        """
        Передача дополнительных параметров в контекст шаблона проекта
        """
        context_data = super().get_context_data()
        user_obj = self.get_object()
        context_data['title'] = f"Профиль пользователя - {user_obj}"
        return context_data


@login_required
def user_generate_new_password_view(request):
    """
    Представление интерфейса для генерации нового пароля пользователя
    """
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


def user_orders(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = user.orders.all()
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)
