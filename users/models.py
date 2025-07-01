from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Модель роли пользователя
    """
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    """
    Модель пользователя
    """

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Задайте уникальное имя
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        related_query_name='custom_user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Задайте уникальное имя
        blank=True,
        help_text='Разрешения, предоставленные пользователю.',
        related_query_name='custom_user'
    )

    username = None
    email = models.EmailField(unique=True, verbose_name='Эл. почта')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='Anonymous')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Представление модели в строковом виде
        """
        return f'{self.email}'

    class Meta:
        """
        Настройка параметров для модели User
        """
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']