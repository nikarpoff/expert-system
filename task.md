# Разработка вероятностной экспертной системы на Python с PostgreSQL

## Цель проекта

Разработать экспертную систему на Python, использующую вероятностную модель Байеса для диагностики заболеваний на основе симптомов пользователя.

Система должна:
- динамически выбирать наиболее информативные вопросы;
- пересчитывать вероятности диагнозов после каждого ответа;
- работать с существующей PostgreSQL-базой данных;
- ввод и отображение информации, из базы данных;
-	вывод принятого решения с указанием вероятности диагноза;
-	возможность пошагового наблюдения за процессом принятия решения.


---

# Технологический стек

## Язык
- Python 3.12+

## База данных
- PostgreSQL

## ORM / SQL
- SQLAlchemy

## GUI
- PyQt6

## Дополнительно
- dataclasses
- pydantic
- loguru
- dotenv
- uv

---

# Архитектура проекта

Проект должен быть построен по модульной архитектуре.

## Структура проекта

```text
expert_system/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories.py
│   │
│   ├── engine/
│   │   ├── bayes_engine.py
│   │   ├── probability_service.py
│   │   ├── symptom_selector.py
│   │   └── diagnosis_filter.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── debug_window.py
│   │   └── widgets/
│   │
│   ├── services/
│   │   ├── diagnosis_service.py
│   │   └── session_service.py
│   │
│   └── utils/
│       ├── logger.py
│       └── math_utils.py
│
├── logs/
├── pyproject.toml
└── README.md
