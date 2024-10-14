# Используем официальный образ PostgreSQL
FROM postgres:16.4

# Копируем файл инициализации в папку для инициализации базы данных
COPY init.sql /docker-entrypoint-initdb.d/

# Указываем переменные окружения для PostgreSQL
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=mydatabase

# Контейнер автоматически выполнит скрипт init.sql при старте
