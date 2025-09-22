# Movies marker ✏️ backend service

## Описание
Учебный проект на FastApi, посвященный хранению пользовательских оценок фильмов. 

## Инструменты, технологии
- FastApi фреймворк
- Место хранения данных - Postgres
- Миграции - alembic
- Тестирование - pytest
- sqlalchemy
- pydantic
- asyncio
- docker-compose
- makefile
- poetry
- github actions


Таблицы: user, movie, marks.
![изображение](https://user-images.githubusercontent.com/8655093/194584977-4761b620-3818-4268-a34b-ad97fcfc1124.png)


API сервиса:
- добавление фильма (название),

- добавление новой оценки фильму,

- изменение поставленной оценки.

## Makefile
- `make up`: запускает docker-compose и миграции
- `make run`: запускает FastApi приложение 
- `make test`: запускает тесты
- `make down`: останавливает контейнеры


![изображение](https://user-images.githubusercontent.com/8655093/197354013-5aec7b62-8e9d-46ef-9c06-9a85171d683d.png)


![изображение](https://user-images.githubusercontent.com/8655093/197353883-37b3aa9d-1b76-4070-be23-2347c962ad40.png)

## Setup
- `pyenv exec python -m venv .venv`
- activate venv
- edit .env
- `poetry install --no-root`
- choose venv/interpreter
- `make async-alembic-up`
