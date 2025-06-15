from django.core.mail import send_mail
from blog.models import AccountVerification


def send_verification_email(user):
    verification = AccountVerification.objects.get(user=user)
    verification_link = f"http://localhost:8000/verify-email/?code={verification.code}"
    subject = 'Подтверждение аккаунта'
    message = f'Для подтверждения аккаунта перейдите по ссылке:\n{verification_link}'
    send_mail(subject, message, 'no-reply@yourdomain.com', [user.email])
