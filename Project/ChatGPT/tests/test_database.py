"""Independent unit tests of database module lifecycle and SQLite schema."""
import sqlite3
from unittest.mock import Mock
import pytest
from sqlalchemy import inspect
from models.models import TodoItem
import database.database as db_module


def test_todo_table_and_column_names(db_session_factory):
    columns = inspect(db_session_factory.kw["bind"]).get_columns("todos")
    assert {c["name"] for c in columns} == {"id", "title", "description", "status"}


def test_primary_key(db_session_factory):
    pk = inspect(db_session_factory.kw["bind"]).get_pk_constraint("todos")
    assert pk["constrained_columns"] == ["id"]


def test_table_uses_sqlite(db_session_factory):
    assert db_session_factory.kw["bind"].dialect.name == "sqlite"


def test_get_db_yields_session_and_closes(monkeypatch):
    fake = Mock()
    monkeypatch.setattr(db_module, "SessionLocal", Mock(return_value=fake))
    gen = db_module.get_db()
    assert next(gen) is fake
    with pytest.raises(StopIteration):
        next(gen)
    fake.close.assert_called_once_with()


def test_get_db_closes_on_generator_close(monkeypatch):
    fake = Mock()
    monkeypatch.setattr(db_module, "SessionLocal", Mock(return_value=fake))
    gen = db_module.get_db()
    assert next(gen) is fake
    gen.close()
    fake.close.assert_called_once_with()
