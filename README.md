# Куда пойти — Москва глазами Артёма

Интерактивная карта Москвы с интересными местами. Кликом по точке на карте открывается боковая панель с описанием и фотографиями места.

<img width="2547" height="1373" alt="image" src="https://github.com/user-attachments/assets/f1635591-c491-48bb-80c7-338d69c1a09a" />


## Запуск

Для запуска проекта вам понадобится Python 3.12+.

Скачайте код с GitHub. Установите виртуальное окружение и зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создайте файл `.env` рядом с `manage.py` на основе `.env.example`:

```bash
cp .env.example .env
```

Создайте базу данных и примените миграции:

```bash
python manage.py migrate
```

Загрузите начальные данные о местах из JSON-файлов:

```bash
python manage.py load_place
```

Создайте суперпользователя для доступа к админке:

```bash
python manage.py createsuperuser
```

Запустите разработческий сервер:

```bash
python manage.py runserver
```

## Импорт данных

Проект умеет загружать данные о местах из JSON-файлов. Команда `load_place` поддерживает два варианта:

**Загрузить все файлы из `static/places/`:**

```bash
python manage.py load_place
```

**Загрузить один файл по пути или URL:**

```bash
python manage.py load_place places/my_place.json
python manage.py load_place https://example.com/place.json
```

Формат JSON-файла:

```json
{
    "title": "Название места",
    "imgs": [
        "https://example.com/photo1.jpg",
        "https://example.com/photo2.jpg"
    ],
    "description_short": "Краткое описание",
    "description_long": "<p>Подробное описание с HTML-разметкой.</p>",
    "coordinates": {
        "lng": "37.649122",
        "lat": "55.777545"
    }
}
```

## Переменные окружения

Настройки проекта берутся из переменных окружения. Создайте файл `.env` рядом с `manage.py` и запишите данные в формате `ПЕРЕМЕННАЯ=значение`.

Доступные переменные:

- `SECRET_KEY` — секретный ключ проекта. Обязательна.
- `DEBUG` — дебаг-режим. Поставьте `True` для разработки.
- `ALLOWED_HOSTS` — разрешённые хосты, через запятую. Обязательна.
- `DATABASE_URL` — URL базы данных. По умолчанию `sqlite:///db.sqlite3`. Обязательна.

Пример `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Инструменты разработки

В файле `requirements-dev.txt` собраны пакеты для разработки:

- **black** — форматирование кода
- **isort** — сортировка импортов
- **flake8** — линтер
- **autoflake** — удаление неиспользуемых импортов
- **djlint** — линтер для HTML/Django-шаблонов
- **pre-commit** — автоматический запуск проверок при коммите

Установка:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
