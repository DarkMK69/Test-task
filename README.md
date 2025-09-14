# Order Service API

REST API сервис для управления заказами, товарами и клиентами.

## Функциональность

- Управление товарами и категориями
- Управление клиентами и заказами
- Добавление товаров в заказы с проверкой наличия
- Иерархическая система категорий с неограниченной вложенностью

## Запуск проекта

### Установка зависимостей
pip install -r requirements.txt

### Запуск PostgreSQL (требуется установленный Docker)
docker run -d --name order_db -p 5432:5432 \
  -e POSTGRES_DB=order_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  postgres:13

### Инициализация данных
python scripts/init_data.py

### Запуск сервера
uvicorn app.main:app --reload

### Требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)

### Запуск через Docker Compose

```bash
# Клонирование репозитория
git clone <repository-url>
cd order_service

# Запуск сервисов
docker-compose up -d

# Остановка сервисов
docker-compose down