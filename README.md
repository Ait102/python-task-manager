# python-task-manager

Консольный менеджер задач на Python. Учебный проект для практики работы с ветками Git.

## Возможности

- добавить задачу;
- показать список задач;
- отметить задачу выполненной;
- удалить задачу.

## Запуск

```bash
python src/main.py
```

## Структура проекта

```
python-task-manager/
├── src/main.py          # код программы
├── tests/test_main.py   # тесты pytest
├── README.md
├── requirements.txt
└── .gitignore
```

## Ветки

- `main` — стабильная версия;
- `feature/*` — разработка отдельных функций, вливаются в `main` через merge.

## Тесты

```bash
pip install -r requirements.txt
python -m pytest
```
