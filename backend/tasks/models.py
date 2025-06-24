from django.db import models
from django.utils import timezone
import shortuuid  # для нестандартных PK


class User(models.Model):
    telegram_id = models.BigIntegerField(
        primary_key=True,
        unique=True,
        verbose_name='Telegram ID'
    )
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )

    def __str__(self):
        return f"{self.username or 'No name'} (ID: {self.telegram_id})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']


class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.ShortUUID().uuid
    )
    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Task(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.ShortUUID().uuid
    )
    title = models.CharField(
        max_length=200
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Таска'
        verbose_name_plural = 'Таски'
        ordering = ['-created_at']
