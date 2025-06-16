import os
from celery import Celery

# Указываем, где находятся настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаём приложение Celery
app = Celery('config')

# Читаем настройки Celery из Django settings (по префиксу CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит tasks.py во всех приложениях
app.autodiscover_tasks()
