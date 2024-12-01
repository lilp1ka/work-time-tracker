FROM python:3.11

WORKDIR /data_processing_service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH="/data_processing_service:/data_processing_service/app:/data_processing_service/backend"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]