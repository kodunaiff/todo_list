FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей в рабочую директорию
COPY requirements.txt .

# Установите зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8080", "wishList.wsgi:application"]