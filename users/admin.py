from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели User
    """
    list_display = ('pk', 'email', 'last_name', 'first_name', 'role')
    list_filter = ('last_name',)
