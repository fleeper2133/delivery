
# Проект с использованием Docker Compose

Этот проект включает в себя три сервиса: базу данных PostgreSQL, бэкенд на Django и фронтенд. Проект использует Docker Compose для управления и оркестрации контейнеров.

## Предварительные требования

- Установленный Docker
- Установленный Docker Compose

## Установка и запуск

1. Клонируйте репозиторий на ваш локальный компьютер.

2. Создайте файл `.env` в корне проекта и настройте необходимые переменные окружения для базы данных и других сервисов.
   Пример содержимого файла `.env`:
 ```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=*

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
   ```

3. Запустите проект с помощью Docker Compose:

   ```bash
docker-compose up --build
   ```

4. После успешного запуска, сервисы будут доступны по следующим адресам:
   - Бэкенд: `http://localhost:8000`
   - Фронтенд: `http://localhost:8080`

## Пользователи

При первом запуске проекта будут автоматически созданы два пользователя:
- **Admin**: Логин `admin`, Пароль `admin`
- **Test**: Логин `test`, Пароль `12345`

## Структура проекта

- `django_api/`: Исходный код бэкенда на Django.
- `frontend/`: Исходный код фронтенда.
- `.env`: Файл с переменными окружения.
- `docker-compose.yml`: Конфигурация Docker Compose для сервисов.

## Дополнительные команды

- Для остановки проекта:

  ```bash
docker-compose down
  ```

- Для выполнения миграций вручную:

  ```bash
docker-compose exec backend python manage.py migrate
  ```

## Лицензия

MIT
