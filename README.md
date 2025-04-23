# Schedule API 🗓️

**FastAPI-приложение для управления расписанием занятий с поддержкой повторяющихся событий**

## 📌 Возможности

- Создание/редактирование/удаление событий расписания
- Поддержка повторяющихся событий:
  - Ежедневные
  - Еженедельные
  - Раз в две недели
  - Ежемесячные
- Проверка конфликтов времени для событий
- JWT-аутентификация с ролевой моделью (админ/пользователь)
- Асинхронное взаимодействие с PostgreSQL
- Автоматическая документация API (Swagger/ReDoc)

## 🛠️ Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Pydantic (валидация данных)
- JWT (аутентификация)

## 🚀 Запуск проекта

### Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```
Создайте файл config.py и добавьте:

```python
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 часа
DATABASE_PASSWORD = "your-password"
DATABASE_LOGIN = "your-login"
POSTGRES_SERVER = "localhost"  # или ваш IP
POSTGRES_PORT = "5432"        # стандартный порт PostgreSQL
```
Запустите сервер:

```bash
uvicorn app.main:app --reload
```
После запуска будет доступно:

API: http://localhost:8000

Документация: http://localhost:8000/docs

Альтернативная документация: http://localhost:8000/redoc

## 📚 Документация API
### Аутентификация
POST /login - Получение JWT-токена

### Расписание
GET /api/schedule/{audience_id}/week/{start_date} - Расписание на неделю

POST /api/schedule - Создать событие (требуется админ)

PUT /api/schedule/{audience_id}/{id} - Обновить событие (админ)

DELETE /api/schedule/{audience_id}/{id} - Удалить событие (админ)

### Пользователи
GET /users/{id} - Получить пользователя по ID

POST /users/admin - Создать админа (требуется админ)

POST /users - Создать обычного пользователя

## 🔒 Аутентификация
Два уровня доступа:

### Администратор:

- Полный доступ ко всем операциям

- Может создавать/редактировать/удалять события

- Может создавать других админов

### Пользователь:

- Только просмотр расписания

- Ограниченный доступ к профилю

## 🗃️ Примеры запросов
### Создание события
POST /api/schedule
```json
{
    "subject": "Математика",
    "teacher": "Иванов И. И.",
    "start_time": "20:00:00",
    "end_time": "22:00:00",
    "repeat_frequency": null, 
    "repeat_until": null, 
    "id": 15,
    "date": "2025-08-09"
}
```
repeat_until - Дата (до какого числа повторение)
repeat_frequency - Частота повторений: daily, weekly, secondweek, monthly

### Создание пользователя
POST /users
```json
{
  "username": "new_user",
  "password": "user123",
}
```
### Аутентификация
POST /login
```json
{
  "username": "admin",
  "password": "secret"
}
```