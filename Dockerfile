FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости системы для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем директории для миграций
RUN mkdir -p app/migrations/versions

EXPOSE 8000

CMD ["sh", "-c", "sleep 3 && python scripts/init_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]