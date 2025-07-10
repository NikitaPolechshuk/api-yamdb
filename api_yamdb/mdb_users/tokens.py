import secrets
from django.core.mail import send_mail
from django.conf import settings


def generate_confirmation_code():
    return secrets.token_urlsafe(32)


def send_confirmation_code(email, confirmation_code):
    subject = "Код подтверждения YaMDb"
    message = f"Ваш код подтверждения: {confirmation_code}"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
