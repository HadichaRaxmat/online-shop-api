# tasks.py
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

@shared_task
def delete_expired_codes():
    from blog.models import DepositPayment  # ✅ Импорт внутри функции
    expiration_time = timezone.now() - timedelta(minutes=5)
    expired = DepositPayment.objects.filter(created_at__lt=expiration_time)
    count = expired.count()
    expired.delete()
    return f"{count} expired codes deleted"
