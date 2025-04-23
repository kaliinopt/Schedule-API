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

Запустите сервер:

uvicorn app.main:app --reload


📚 Документация API
Все эндпоинты доступны через Swagger UI:
GET /docs

Основные роуты:

POST /api/auth/login - Получение JWT-токена

GET /api/schedule/{audience_id}/{date} - Получить расписание на дату

POST /api/schedule - Создать новое событие (требуются права админа)

PUT /api/schedule/{audience_id}/{id} - Обновить событие (требуются права админа)

🔒 Аутентификация
Используется JWT с двумя ролями:

Админ (может создавать/редактировать/удалять события)

Пользователь (только просмотр)

Пример запроса для получения токена:

json
POST /api/auth/login
{
  "username": "admin",
  "password": "secret"
}

config.py файл
DEBUG=True
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_DB=schedule_db
SECRET_KEY=your-secret-key
🤝 Как внести вклад
Форкните репозиторий

Создайте ветку для вашей фичи (git checkout -b feature/amazing-feature)

Сделайте коммит изменений (git commit -m 'Add some amazing feature')

Запушьте ветку (git push origin feature/amazing-feature)

Откройте Pull Request

📄 Лицензия
MIT

### Советы по адаптации: