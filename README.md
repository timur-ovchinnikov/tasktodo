# tasktodo
Тестовое задание ToDo

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

## Выполнение миграций

Если вы используете Docker, выполните миграции внутри контейнера приложения:

```bash
docker exec -it todo_app alembic upgrade head
```

Это создаст необходимые таблицы в базе данных.

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
-d '{"title": "New Task", "description": "Task description", "due_date": "2023-12-31T23:59:59"}'
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
