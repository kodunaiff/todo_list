from celery import shared_task
from django.utils import timezone
from .models import Task
import logging
from aiogram import Bot
import os


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


@shared_task
def check_due_tasks():
    now = timezone.now()
    tasks = Task.objects.filter(
        due_date__lte=now,
        status='pending'
    ).select_related('user')

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        return

    bot = Bot(token=bot_token)

    for task in tasks:
        try:
            bot.send_message(
                chat_id=task.user.telegram_id,
                text=f"⏰ Задача просрочена: {task.title}\n"
                     f"📅 Срок выполнения: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n"
                     f"📝 Описание: {task.description or 'Нет описания'}"
            )
            task.status = Task.Status.OVERDUE
            task.save()
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
