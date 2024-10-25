# Базовый образ Python
FROM python:3.11

# Установка рабочей директории
WORKDIR /service

# Копирование файла с зависимостями
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов микросервиса в контейнер
COPY . .

# Команда для запуска приложения (FastAPI или другое)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
