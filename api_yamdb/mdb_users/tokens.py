import secrets

from django.conf import settings
from django.core.mail import send_mail

from api_yamdb.exceptions import SendConfirmationCodeError


def generate_confirmation_code():
    return secrets.token_urlsafe(settings.CONFIRMATION_CODE_BYTES_LENGTH)


def send_confirmation_code(email, confirmation_code):
    subject = 'Код подтверждения YaMDb'
    message = f'Ваш код подтверждения: {confirmation_code}'

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        raise SendConfirmationCodeError(('Ошибка при отправке кода '
                                        f'подтверждения: {e}')) from e
