from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    """
    Отправка сообщения об успешной регистрации пользователем
    """
    send_mail(
        subject="Поздравляем с регистрацией на нашем сервисе",
        message="Вы успешно зарегистрировались на нашей платформе",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_new_password(email, new_password):
    """
    Отправка сообщения об успешном изменении пароля пользователем
    """
    send_mail(
        subject="Вы успешно изменили пароль",
        message=f"Ваш новый пароль: {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
