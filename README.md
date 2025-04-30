# BonoAppetito
[![BonoAppetito workflow](https://github.com/shft1/BonoAppetito/actions/workflows/main.yml/badge.svg)](https://github.com/shft1/BonoAppetito/actions/workflows/main.yml)

---

### Оглавление
- [Ссылка на сайт](#ссылка-на-сайт---httpsbonoappetitoru)
- [Описание](#описание)
- [Стек технологий](#стек-технологий)
- [Презентация проекта](#проект-состоит-из-следующих-страниц)
- [Права пользователей](#разграничение-прав-пользователей)
- [Инструкция по развертыванию](#инструкция-по-развертыванию)
  - [Локальный запуск приложения](#локальный-запуск-приложения)
  - [Запуск на сервере](#запуск-приложения-на-сервере)
- [Процесс CI/CD](#процесс-cicd)
- [Автор](#%EF%B8%8F-автор)

---

### Ссылка на сайт - https://bonoappetito.ru/recipes

---

### Описание:
Проект BonoAppetito представляет собой веб-приложение, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

---

### Стек технологий:
Python, Django REST Framework, Docker, Docker Compose, Nginx, GitHub Actions (CI/CD), PostgreSQL, SQLite, React.

---

### Проект состоит из следующих страниц: 

_**Главная страница**_

<img width="732" alt="image" src="https://github.com/user-attachments/assets/cfe07096-2759-4f7d-9999-e45983c79e2c" />

_**Страница входа**_

<img width="1210" alt="image" src="https://github.com/user-attachments/assets/e35903c1-93f1-41c9-8d76-8c67af964547" />

_**Страница регистрации**_

<img width="1199" alt="image" src="https://github.com/user-attachments/assets/b24c6c12-9df7-4536-9212-2e353461c6b4" />

_**Страница рецепта**_

<img width="1247" alt="image" src="https://github.com/user-attachments/assets/785376d3-b3db-4480-a7c7-69cc53cee9c7" />

_**Страница пользователя**_

<img width="1236" alt="image" src="https://github.com/user-attachments/assets/607df7d9-3c6f-4921-bad9-9fed57261a96" />

_**Страница подписок**_

<img width="1219" alt="image" src="https://github.com/user-attachments/assets/61af977b-c2eb-4176-b047-77487a4e1ff2" />

_**Избранное**_

<img width="1226" alt="image" src="https://github.com/user-attachments/assets/77dadf93-64fd-41ff-9368-9ebb5ddc73e4" />

_**Список покупок**_

<img width="1214" alt="image" src="https://github.com/user-attachments/assets/23c848b4-4ff4-4f03-8efd-39ffd2fab210" />

_**Собранный список ингредиентов**_

<img width="366" alt="image" src="https://github.com/user-attachments/assets/7c5122ff-850e-44e2-aee0-6e0ff1135182" />

_**Создание и редактирование рецепта**_

<img width="1042" alt="image" src="https://github.com/user-attachments/assets/82d9449a-0abe-418c-9bfe-df63c2aa1489" />

_**Редактирование рецепта**_

<img width="660" alt="image" src="https://github.com/user-attachments/assets/627aaaf9-ac34-43fe-a35e-637b45bc1c2f" />

_**Страница смены пароля**_

<img width="1201" alt="image" src="https://github.com/user-attachments/assets/4d098a45-73c2-44de-be0c-4990a89aa1e3" />

---

### Разграничение прав пользователей
В проекте описаны разные уровни доступа пользователей:  
- гость (анонимный пользователь),
- аутентифицированный (залогиненный) пользователь,
- администратор.

<img width="755" alt="image" src="https://github.com/user-attachments/assets/d1facfba-4c1e-4576-9541-c722e81f81ad" />

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

---

### Локальный запуск приложения

**Запустите Docker Compose командой:**
```
docker compose -f docker-compose.infra.yml up
```

**В контейнере `backend` зайдите в терминал:**
```
docker compose -f docker-compose.infra.yml exec -it backend bash
```

**В нем выполните следующие команды**
- `python manage.py migrate` - выполнить миграции
- `python manage.py collectstatic` - сбор статики Django
- `cp -r /app/collected_static/. /backend_static/static/` - копирование в папку
- `filler_ingredients.py` - скрипт, для заполнения исходными данными таблицу с ингредиентами

**Откройте приложение, обратившись по адресу http://127.0.0.1**

---

### Запуск приложения на сервере

1. Перейдите в `settings` репозитория `BonoAppetito`
2. Перейдите по -> `Security` -> `Secrets and variables` -> `Actions`
3. Заполните `Repository secrets` следующим образом:
   ```
   - DOCKER_PASSWORD - Ваш пароль от DockerHub
   - DOCKER_USERNAME - Ваше username на DockerHub
   - HOST - IP-адрес вашего удаленного сервера
   - SSH - закрытый SSH-ключ
   - SSH_PASSPHRASE - Пароль от закрытого SSH-ключа
   - USER - Имя пользователя на сервере
   ```
4. Сделайте `git push` в ветку `main`, чтобы запустить процесс CI/CD

---

### Процесс CI/CD:
При создании `git push` в ветку `main` запускается процесс CI/CD, который: 
1. Проверяет `backend-` и `frontend-код` линтером и запускает автотесты
2. После успешной проверки, собирает образы `backend`, `frontend`, `gateway` и пушит их на `DockerHub`
3. Подключается по `SSH` к серверу и выполняет несколько шагов шага:
   - Копирует файл `docker-compose.production.yml` на сервер
   - Стягивает образы с `DockerHub`
   - Пересобирает контейнеры из новых образов
   - Собирает статику контейнера `backend`
4. Заполните исходными данными таблицу с ингредиентами, для этого, на удаленном сервере, выполните команду:  
   `docker compose -f docker-compose.production.yml exec backend python filler_ingredients.py`

---

### ✏️ Автор 
**Алексей Малков - [Ссылка на GitHub](https://github.com/shft1)**
