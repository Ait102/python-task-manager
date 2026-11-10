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


def test_save_and_load(tmp_path):
    path = tmp_path / "tasks.json"
    main.add_task("Сохранить меня")
    main.complete_task(1)
    main.save_tasks(path)
    main.tasks.clear()
    main.load_tasks(path)
    assert main.list_tasks() == [{"id": 1, "title": "Сохранить меня", "done": True}]


def test_load_missing_or_broken_file(tmp_path):
    main.add_task("A")
    main.load_tasks(tmp_path / "nope.json")
    assert main.list_tasks() == []
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    main.load_tasks(bad)
    assert main.list_tasks() == []


def test_menu_handles_bad_input(monkeypatch, capsys):
    answers = iter(["1", "   ", "3", "abc", "1", "Купить хлеб", "7", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    monkeypatch.setattr(main, "save_tasks", lambda path=None: None)
    monkeypatch.setattr(main, "load_tasks", lambda path=None: None)
    main.main()
    out = capsys.readouterr().out
    assert "Ошибка: Название задачи не может быть пустым" in out
    assert "Ошибка: Номер задачи должен быть целым числом" in out
    assert "Всего: 1, выполнено: 0, осталось: 1" in out
