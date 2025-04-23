# Schedule API 🗓️

FastAPI-приложение для управления расписанием занятий с поддержкой повторяющихся событий.

## 📌 Возможности

- Создание/редактирование/удаление событий расписания
- Поддержка повторяющихся событий (ежедневные, еженедельные, раз в две недели, ежемесячные)
- Проверка конфликтов времени для событий
- JWT-аутентификация и ролевая модель (админ/пользователь)
- Асинхронное взаимодействие с PostgreSQL
- Документация API (Swagger/ReDoc)

## 🛠️ Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Pydantic (валидация данных)
- JWT (аутентификация)

## 🚀 Запуск проекта
### Локальная разработка

```bash

API: http://localhost:8000

Документация: http://localhost:8000/docs

Альтернативная docs: http://localhost:8000/redoc 

Установите зависимости:

pip install -r requirements.txt

Создайте файл config.py и добавьте
SECRET_KEY = your-secret-key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = your-expire
DATABASE_PASSWORD = your-password
DATABASE_LOGIN = your-login
POSTGRES_SERVER = your-ip
POSTGRES_PORT = your-port

Запустите сервер:

uvicorn app.main:app --reload

📚 Документация API
Все эндпоинты доступны через Swagger UI:
GET /docs

Основные роуты:

POST /login - Получение JWT-токена

GET /api/schedule/{audience_id}/week/{start_date} - Получить расписание на неделю вперед

POST /api/schedule - Создать новое событие (требуются права админа)

PUT /api/schedule/{audience_id}/{id} - Обновить событие (требуются права админа)

🔒 Аутентификация
Используется JWT с двумя ролями:

Админ (может создавать/редактировать/удалять события)

Пользователь (только просмотр)

Пример запроса для получения токена:

json
POST /login
{
  "username": "admin",
  "password": "secret"
}
