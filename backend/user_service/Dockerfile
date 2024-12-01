FROM python:3.11

WORKDIR /user_service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH="/user_service:/user_service/app:/user_service/backend"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]