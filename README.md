# expert-system

Вероятностная экспертная система для медицинской диагностики на Python + PostgreSQL + PyQt6.

## Запуск

1. Создайте БД PostgreSQL и примените `create-db.sql`.
2. Создайте `.env` (пример):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expert_system
DB_USER=postgres
DB_PASSWORD=postgres
DECISION_THRESHOLD=0.95
EXCLUSION_THRESHOLD=0.01
```

3. Установите зависимости и запустите:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
expert-system
```

## Что реализовано

- загрузка диагнозов, симптомов и правил из PostgreSQL через SQLAlchemy;
- байесовское обновление вероятностей после каждого ответа;
- выбор следующего вопроса по информативности;
- исключение маловероятных диагнозов;
- ранняя остановка при достижении порога уверенности;
- GUI на PyQt6 с отображением текущих вероятностей;
- отдельное окно отладки с пошаговым логом принятия решений.
