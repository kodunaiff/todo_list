from rest_framework import viewsets
from .models import Task, Category, User
from .serializers import TaskSerializer, CategorySerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create_or_get_user(self, telegram_id, username=None):
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': username}
        )
        return user

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # Получаем или создаем пользователя
        telegram_id = self.request.data.get('user')
        username = self.request.data.get('username')
        user = UserViewSet().create_or_get_user(telegram_id, username)

        # Сохраняем задачу с привязкой к пользователю
        serializer.save(user=user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
