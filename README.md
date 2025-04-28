# TaskTodo

A modern task management API built with FastAPI, PostgreSQL, and Redis.

## Features

- User authentication with JWT tokens
- Task management (create, read, update, delete)
- Task filtering and sorting
- Pagination support
- Email notifications for upcoming tasks
- Redis caching for improved performance
- Comprehensive logging
- CI/CD pipeline with GitHub Actions
- Docker support for easy deployment

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Redis
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tasktodo.git
cd tasktodo
```

2. Create a `.env` file with the following variables:
```env
DATABASE_URL=postgresql://todo_user:todo_password@postgres:5432/todo_db
REDIS_URL=redis://redis:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

3. Start the services:
```bash
docker-compose up --build
```

4. Run database migrations:
```bash
docker exec -it tasktodo_app alembic upgrade head
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the tests with:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=app
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Отладка

### Конфликт имен контейнеров

Если вы видите ошибку, связанную с конфликтом имен контейнеров, выполните следующие шаги:

1. Удалите конфликтующий контейнер:
   ```bash
   docker rm -f <CONTAINER_NAME>
   ```
   Например:
   ```bash
   docker rm -f todo_postgres
   ```

2. Перезапустите сервисы:
   ```bash
   docker-compose up --build
   ```

3. Если проблема сохраняется, используйте флаг `--remove-orphans`:
   ```bash
   docker-compose up --build --remove-orphans
   ```

### Проблемы с подключением к базе данных

Если вы видите ошибку `password authentication failed for user`, выполните следующие шаги:

1. Убедитесь, что в `docker-compose.yml` указаны правильные значения для:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`

2. Проверьте файл `alembic.ini` и убедитесь, что `sqlalchemy.url` соответствует этим значениям:
   ```ini
   sqlalchemy.url = postgresql+psycopg2://todo_user:todo_password@postgres:5432/todo_db
   ```

3. Проверьте файл `env.py` и убедитесь, что он использует переменную окружения `DATABASE_URL`.

4. Удалите старые контейнеры и данные:
   ```bash
   docker-compose down -v
   ```

5. Перезапустите сервисы:
   ```bash
   docker-compose up --build
   ```

6. Выполните миграции:
   ```bash
   docker exec -it todo_app alembic upgrade head
   ```

## Использование API через curl

### Регистрация пользователя
```bash
curl -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "password123"}'
```

### Авторизация и получение токена
```bash
curl -X POST http://localhost:8000/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user@example.com&password=password123"
```

### Создание задачи
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"title": "New Task", "description": "Task description", "due_date": "2025-12-31T23:59:59"}'
```

### Получение списка задач
```bash
curl -X GET http://localhost:8000/api/v1/tasks/ \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Получение задачи по ID
```bash
curl -X GET http://localhost:8000/api/v1/tasks/<TASK_ID> \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Удаление задачи
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/<TASK_ID> \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

> Замените `<ACCESS_TOKEN>` на ваш токен, полученный при авторизации, и `<TASK_ID>` на ID задачи.
