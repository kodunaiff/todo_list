# todo_app/serializers.py
from rest_framework import serializers
from .models import Task, Category, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'username', 'created_at']
        read_only_fields = ['created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'category_id', 'user', 'created_at', 'due_date',
                  'is_completed']
