import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import main  # noqa: E402


@pytest.fixture(autouse=True)
def clear_tasks():
    main.tasks.clear()


def test_add_task():
    task = main.add_task("Купить хлеб")
    assert task == {"id": 1, "title": "Купить хлеб", "done": False}


def test_list_tasks():
    main.add_task("A")
    main.add_task("B")
    assert [t["title"] for t in main.list_tasks()] == ["A", "B"]


def test_complete_task():
    main.add_task("A")
    assert main.complete_task(1) is True
    assert main.list_tasks()[0]["done"] is True
    assert main.complete_task(99) is False


def test_delete_task():
    main.add_task("A")
    assert main.delete_task(1) is True
    assert main.list_tasks() == []
    assert main.delete_task(1) is False


def test_get_stats():
    main.add_task("A")
    main.add_task("B")
    main.complete_task(1)
    assert main.get_stats() == {"total": 2, "done": 1, "left": 1}


@pytest.mark.parametrize("title", ["", "   ", "x" * 101])
def test_add_task_rejects_bad_title(title):
    with pytest.raises(ValueError):
        main.add_task(title)


def test_add_task_strips_title():
    assert main.add_task("  Задача  ")["title"] == "Задача"


def test_ids_unique_after_delete():
    main.add_task("A")
    main.add_task("B")
    main.delete_task(1)
    assert main.add_task("C")["id"] == 3


@pytest.mark.parametrize("value, expected", [("3", 3), (" 7 ", 7)])
def test_parse_task_id_ok(value, expected):
    assert main.parse_task_id(value) == expected


@pytest.mark.parametrize("value", ["abc", "", "0", "-2", "1.5"])
def test_parse_task_id_bad(value):
    with pytest.raises(ValueError):
        main.parse_task_id(value)


def test_search_tasks():
    main.add_task("Купить молоко")
    main.add_task("Сделать лабу по Git")
    main.add_task("купить хлеб")
    assert [t["id"] for t in main.search_tasks("КУПИТЬ")] == [1, 3]
    assert main.search_tasks("нет такого") == []


def test_filter_tasks():
    main.add_task("A")
    main.add_task("B")
    main.complete_task(2)
    assert [t["id"] for t in main.filter_tasks(True)] == [2]
    assert [t["id"] for t in main.filter_tasks(False)] == [1]
