from rest_framework import viewsets, status
from .models import Task, Category, User
from .serializers import TaskSerializer, CategorySerializer, UserSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        username = request.data.get('username', None)

        if not telegram_id:
            return Response(
                {"error": "telegram_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': username}
        )

        if created:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
