"""Python Task Manager (TaskMan) — менеджер задач для командной строки."""

import json
from pathlib import Path

__version__ = "1.2.0"

DATA_FILE = Path("tasks.json")

tasks = []


def validate_title(title):
    """Проверяет название задачи и возвращает его без лишних пробелов."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Название задачи не может быть пустым")
    if len(title.strip()) > 100:
        raise ValueError("Название задачи длиннее 100 символов")
    return title.strip()


def parse_task_id(value):
    """Преобразует ввод пользователя в номер задачи (целое число > 0)."""
    try:
        task_id = int(str(value).strip())
    except ValueError:
        raise ValueError("Номер задачи должен быть целым числом") from None
    if task_id <= 0:
        raise ValueError("Номер задачи должен быть больше нуля")
    return task_id


def add_task(title):
    """Добавляет задачу и возвращает её."""
    title = validate_title(title)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": task_id, "title": title, "done": False}
    tasks.append(task)
    return task


def list_tasks():
    """Возвращает список всех задач."""
    return list(tasks)


def complete_task(task_id):
    """Отмечает задачу выполненной. Возвращает True, если задача найдена."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def delete_task(task_id):
    """Удаляет задачу. Возвращает True, если задача найдена."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False


def get_stats():
    """Возвращает статистику: всего задач, выполнено, осталось."""
    done = sum(1 for task in tasks if task["done"])
    return {"total": len(tasks), "done": done, "left": len(tasks) - done}


def search_tasks(query):
    """Ищет задачи, в названии которых есть строка query (без учёта регистра)."""
    query = query.strip().lower()
    return [task for task in tasks if query in task["title"].lower()]


def filter_tasks(done):
    """Возвращает выполненные (done=True) или невыполненные (done=False) задачи."""
    return [task for task in tasks if task["done"] is done]


def save_tasks(path=DATA_FILE):
    """Сохраняет задачи в JSON-файл."""
    Path(path).write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def load_tasks(path=DATA_FILE):
    """Загружает задачи из JSON-файла. Если файла нет или он повреждён, список пуст."""
    tasks.clear()
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return
    tasks.extend(t for t in data if isinstance(t, dict) and {"id", "title", "done"} <= t.keys())


def format_task(task):
    mark = "x" if task["done"] else " "
    return f"[{mark}] {task['id']}. {task['title']}"


MENU = f"""
=== Python Task Manager v{__version__} ===
1. Добавить задачу
2. Показать задачи
3. Отметить выполненной
4. Удалить задачу
5. Найти задачу
6. Показать выполненные / невыполненные
7. Статистика
0. Выход
"""


def print_tasks(items, empty="Задач нет."):
    if not items:
        print(empty)
    for task in items:
        print(format_task(task))


def handle(choice):
    """Выполняет пункт меню. Возвращает False, если нужно выйти."""
    if choice == "1":
        task = add_task(input("Название задачи: "))
        print(f"Добавлено: {format_task(task)}")
    elif choice == "2":
        print_tasks(list_tasks(), "Список задач пуст.")
    elif choice in ("3", "4"):
        task_id = parse_task_id(input("Номер задачи: "))
        action = complete_task if choice == "3" else delete_task
        print("Готово." if action(task_id) else "Задача не найдена.")
    elif choice == "5":
        print_tasks(search_tasks(input("Что искать: ")), "Ничего не найдено.")
    elif choice == "6":
        done = input("Показать выполненные? (д/н): ").strip().lower() in ("д", "y", "да", "yes")
        print_tasks(filter_tasks(done))
    elif choice == "7":
        stats = get_stats()
        print(f"Всего: {stats['total']}, выполнено: {stats['done']}, осталось: {stats['left']}")
    elif choice == "0":
        return False
    else:
        print("Неизвестный пункт меню.")
    return True


def main():
    load_tasks()
    while True:
        print(MENU)
        try:
            if not handle(input("Выберите пункт: ").strip()):
                break
        except ValueError as error:
            print(f"Ошибка: {error}")
        save_tasks()
    print("Задачи сохранены. До свидания!")


if __name__ == "__main__":
    main()
