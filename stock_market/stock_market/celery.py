import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_market.settings")

celery_app = Celery("stock_market")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
