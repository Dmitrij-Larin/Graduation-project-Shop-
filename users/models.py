from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.models import Order

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Модель роли пользователя
    """
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class UserManager(BaseUserManager):
    """
    Модель создания пользователей
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен быть членом персонала.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен быть суперпользователем.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(unique=True, verbose_name='Эл. почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='Anonymous')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)

    # Связь с заказами
    orders = models.ManyToManyField(Order, related_name='users', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Указываем свой менеджер

    def __str__(self):
        return self.email
