# backend/auth_service/Dockerfile
FROM python:3.11

WORKDIR /auth_service
# долбаеб надо чекнуть что там за пути ls
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# кароче тут прикол у тебя
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]