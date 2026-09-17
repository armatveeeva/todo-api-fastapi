# Todo API — RESTful-сервис для управления задачами

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

RESTful API для управления задачами, реализованный на FastAPI с использованием PostgreSQL в качестве хранилища данных. Проект демонстрирует принципы построения production-ready backend-сервиса: валидация данных через Pydantic V2, миграции схемы БД через Alembic, контейнеризация через Docker и автоматизированное тестирование с изоляцией внешних зависимостей.

## Описание предметной области

Система реализует классический CRUD-интерфейс для управления списком задач (todo-лист) с поддержкой бизнес-логики фильтрации и пагинации. Архитектура проекта спроектирована как учебный шаблон для отработки ключевых компетенций backend-разработки:

- Проектирование RESTful API с соблюдением принципов идемпотентности и согласованности HTTP-методов.
- Работа с реляционной базой данных через ORM (SQLAlchemy 2.0) и управление схемой через миграции (Alembic).
- Валидация входных данных на уровне модели (Pydantic V2) с генерацией понятных сообщений об ошибках.
- Написание unit-тестов с мокированием внешних зависимостей (например, сервисов отправки уведомлений) через `unittest.mock`.
- Контейнеризация приложения и базы данных для воспроизводимого развёртывания.

## Технологический стек

- **Язык программирования:** Python 3.11+
- **Web-фреймворк:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Валидация данных:** Pydantic V2
- **База данных:** PostgreSQL 15
- **Миграции схемы БД:** Alembic
- **Тестирование:** Pytest, `unittest.mock`
- **Контейнеризация:** Docker, Docker Compose
- **Интерактивная документация:** Swagger UI (OpenAPI 3.0, генерируется автоматически)

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose (рекомендуемый способ запуска)
- Либо Python 3.11+ и локально установленный PostgreSQL 15

### Запуск через Docker

1. Клонируйте репозиторий:
```bash
git clone https://github.com/armatveeeva/todo-api.git
cd todo-api
