from django.utils import timezone
from django.core.management.base import BaseCommand
from blog.models import DepositPayment  # замени на нужную модель, если не та

from datetime import timedelta

class Command(BaseCommand):
    help = 'Удаляет OTP-коды, срок действия которых истёк'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(minutes=5)
        deleted_count, _ = DepositPayment.objects.filter(created_at__lt=expiration_time).delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено истёкших OTP-кодов: {deleted_count}'))
