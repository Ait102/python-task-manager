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


def main():
    add_task("Изучить git branch")
    add_task("Сделать лабораторную работу")
    complete_task(1)
    for task in list_tasks():
        print(format_task(task))


if __name__ == "__main__":
    main()
