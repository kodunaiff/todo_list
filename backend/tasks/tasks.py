from celery import shared_task
from django.utils import timezone
from .models import Task
from datetime import timedelta
import logging


@shared_task
def debug_task():
    print("Beat is working!")
    return True


@shared_task
def notify_due_tasks():
    now = timezone.now()
    due_tasks = Task.objects.filter(due_date__lte=now, is_completed=False)
    logging.info("pdjgkglf")


    for task in due_tasks:
        logging.info("pdjgkglf")
        print(f"⚠️ Напоминание пользователю {task.user_id} о задаче: {task.title}")
