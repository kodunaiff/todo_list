from django.contrib import admin
from .models import Task, Category, User

admin.site.register(Task)
admin.site.register(Category)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'created_at')
    search_fields = ('telegram_id', 'username')
