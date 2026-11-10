"""Python Task Manager (TaskMan) — менеджер задач для командной строки."""

__version__ = "1.1.0"

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


def format_task(task):
    mark = "x" if task["done"] else " "
    return f"[{mark}] {task['id']}. {task['title']}"


def main():
    add_task("Изучить git branch")
    add_task("Сделать лабораторную работу")
    complete_task(1)
    for task in list_tasks():
        print(format_task(task))
    stats = get_stats()
    print(f"Всего: {stats['total']}, выполнено: {stats['done']}, осталось: {stats['left']}")


if __name__ == "__main__":
    main()
