"""Консольный менеджер задач."""

tasks = []


def add_task(title):
    """Добавляет задачу и возвращает её."""
    task = {"id": len(tasks) + 1, "title": title, "done": False}
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


def format_task(task):
    mark = "x" if task["done"] else " "
    return f"[{mark}] {task['id']}. {task['title']}"


MENU = """
=== Менеджер задач ===
1. Добавить задачу
2. Показать задачи
3. Отметить выполненной
4. Удалить задачу
0. Выход
"""


def main():
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            task = add_task(input("Название задачи: ").strip())
            print(f"Добавлено: {format_task(task)}")
        elif choice == "2":
            if not tasks:
                print("Список задач пуст.")
            for task in list_tasks():
                print(format_task(task))
        elif choice in ("3", "4"):
            task_id = int(input("Номер задачи: "))
            action = complete_task if choice == "3" else delete_task
            print("Готово." if action(task_id) else "Задача не найдена.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
