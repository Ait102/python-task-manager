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
