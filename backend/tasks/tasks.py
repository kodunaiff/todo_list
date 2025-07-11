from celery import shared_task
from django.utils import timezone
from .models import Task
import requests
import logging
import os
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')


@shared_task
def notify_due_tasks():
    now = timezone.now()
    due_tasks = Task.objects.filter(due_date__lte=now, is_completed=False)

    for task in due_tasks:
        # print(f"⚠️ Напоминание пользователю {task.user_id} о задаче: {task.tit      le}")
        send_telegram_notification.delay(
            chat_id=task.user.telegram_id,
            text=f"⏰ Задача просрочена: {task.title}"
        )


@shared_task
def send_telegram_notification(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={'chat_id': chat_id, 'text': text}
    )
