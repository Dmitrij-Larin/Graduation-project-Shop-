from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class StyleFromMixin:
    """
    Стилизация к полям формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFromMixin, forms.ModelForm):
    """
    Форма пользователя
    """
    class Meta:
        """
        Класс с настройками для модели User
        """
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar',)


class UserRegisterForm(StyleFromMixin, UserCreationForm):
    """
    Форма регистрации пользователя
    """
    class Meta:
        """
        Класс с настройками для модели User
        """
        model = User
        fields = ('email',)

    def clean_password2(self):
        """
        Проверку корректности введённых паролей пользователем
        """
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password1'])
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data['password2']


class UserLoginForm(StyleFromMixin, AuthenticationForm):
    """
    Форма логина пользователя
    """
    pass


class UserUpdateForm(StyleFromMixin, forms.ModelForm):
    """
    Форма обновления данных пользователя
    """
    class Meta:
        """
        Класс с настройками для модели User
        """
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')


class UserPasswordChangeForm(StyleFromMixin, PasswordChangeForm):
    """
    Форма изменения пароля пользователя
    """
    def clean_new_password2(self):
        """
        Изменение пароля
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2, self.user)
        return password2