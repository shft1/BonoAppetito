# Веб-приложение Foodgram

[![Main Kitty workflow](https://github.com/shft1/kittygram_final/actions/workflows/main.yml/badge.svg)](https://github.com/shft1/kittygram_final/actions/workflows/main.yml)

## О проекте:
Проект Foodgram представляет собой веб-приложение, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Стек технологий:
- Djando
- DRF
- React
- Docker
- PostgresSQL
- GitHub Actions (CI/CD)

## Как развернуть проект:
- Установить Docker
- Заполнить файл env
- Запустить docker compose
- В контейнере backend:
    - Выполнить миграции `python manage.py migrate`
    - Собрать статику django `python manage.py collectstatic`
    - Скопировать в папку `cp -r /app/collected_static/. /backend_static/static/`
    - Выполнить файл `filler_ingredients.py` для заполнения исходными данными таблицу с ингредиентами

## Как заполнить файл env ?:
- POSTGRES_DB - имя базы данных (если не указано, то вместо PostgreSQL - SQLite)
- POSTGRES_USER - имя пользователя с правами к базе
- POSTGRES_PASSWORD - пароль пользователя
- DB_NAME - имя контейнера, в котором запущена СУБД
- DB_PORT - порт, на котором работает контейнер с СУБД
- DJANGO_SECRET_KEY - для секретного ключа
- DEBUG - что включения режима отладки значение True/true
- ALLOWED_HOSTS - разрешенные хосты

## Примечание:
При каждом пуше в ветку `master` запускается `.github/workflows/main.yml`, который проверяет backend код линтером и запускает автотесты, затем пушит образы backend, frontend, gateway на DockerHub
(Для этого нужно добавить secrets в настройках репозитория)

## Автор 
Алексей Малков
[Ссылка на гитхаб](https://github.com/shft1)
