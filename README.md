# BonoAppetito
[![BonoAppetito workflow](https://github.com/shft1/BonoAppetito/actions/workflows/main.yml/badge.svg)](https://github.com/shft1/BonoAppetito/actions/workflows/main.yml)

---

### Описание:
Проект BonoAppetito представляет собой веб-приложение, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Стек технологий:
Python, Django REST Framework, Docker, Docker Compose, Nginx, GitHub Actions, PostgreSQL, SQLite, React
.
---

### Инструкция по развертыванию:
**Клонируйте репозиторий:**

```
git clone git@github.com:shft1/BonoAppetito.git
```

**Cоздайте и активируйте виртуальное окружение:**

```
python3 -m venv venv
```
* _Если у вас Linux/macOS_
    ```
    source venv/bin/activate
    ```
* _Если у вас Windows_
    ```
    source venv/scripts/activate
    ```

**Установите зависимости из файла requirements.txt:**

```
pip install -r requirements.txt
```

**Заполните файл .env в корне проекта:**
```
POSTGRES_DB - имя базы данных (если не указать, то БД - SQLite)
POSTGRES_USER - имя пользователя с правами к базе
POSTGRES_PASSWORD - пароль пользователя
DB_HOST - имя контейнера, в котором запущена СУБД
DB_PORT - порт, на котором работает контейнер с СУБД
DJANGO_SECRET_KEY - для секретного ключа
DEBUG - что включения режима отладки значение True/true
ALLOWED_HOSTS - разрешенные хосты
```

**Запустите оркестрацию командой:**
```
docker compose -f docker-compose.infra.yml up
```

**В контейнере `backend` зайдите в терминал:**
```
docker compose -f docker-compose.infra.yml exec -it backend bash
```

**В контейнере выполнить следующие команды**
- `python manage.py migrate` - выполнить миграции
- `python manage.py collectstatic` - сбор статики Django
- `cp -r /app/collected_static/. /backend_static/static/` - копирование в папку
- `filler_ingredients.py` - скрипт, для заполнения исходными данными таблицу с ингредиентами

---

### Примечание:
При каждом пуше в ветку `master` запускается процесс CI/CD, который проверяет backend код линтером и запускает автотесты, затем собирает образы backend, frontend, gateway и пушит их на DockerHub  
_(Для этого нужно добавить secrets в настройках репозитория)_


### Демонстрация возможностей
**_В проекте доступна система регистрации и аутентификации пользователей._**
<img width="1129" alt="image" src="https://github.com/user-attachments/assets/7ce659d2-2827-4bb8-8c4b-6b1c0b4144e7" />

**_После регистрации пользователь переадресовывается на страницу входа._**
<img width="1101" alt="image" src="https://github.com/user-attachments/assets/b8d854a8-4b21-4911-a71d-272209795e9c" />




### Автор 
Алексей Малков
[Ссылка на гитхаб](https://github.com/shft1)
