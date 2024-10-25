FROM mongo:latest

# Устанавливаем утилиты для работы с MongoDB
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -qO - https://www.mongodb.org/static/pgp/server-8.0.asc | apt-key add - && \
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list && \
    apt-get update && \
    apt-get install -y mongodb-org-shell && \
    apt-get clean

# Создаём директорию для данных MongoDB
RUN mkdir -p /data/db

# Определяем рабочую директорию
WORKDIR /data

# Открываем порт MongoDB
EXPOSE 27017

# Запуск MongoDB
CMD ["mongod", "--bind_ip_all"]
