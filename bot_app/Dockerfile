FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=America/Adak

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей в рабочую директорию
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы проекта в рабочую директорию
COPY . /app

# Команда для запуска бота
#CMD ["python", "-m", "bot_app.main"]
CMD ["python", "main.py"]