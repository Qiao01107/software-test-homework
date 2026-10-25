"""Isolated FastAPI tests: fresh SQLite file per test, never original todo.db.

Source under test is loaded from working/app without edits. Each request gets a fresh
SQLAlchemy session, exactly like the production dependency. The project import may
create working/app/todo.db; that path is distinct from the uploaded/original file.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base, get_db
from main import app


@pytest.fixture
def db_session_factory(tmp_path):
    database_path = tmp_path / "isolated_test.sqlite3"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    yield factory
    engine.dispose()


@pytest.fixture
def client(db_session_factory):
    def test_get_db():
        session = db_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = test_get_db
    # Capture 500s as HTTP responses so defect probes remain deterministic.
    try:
        with TestClient(app, raise_server_exceptions=False) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def create_todo(client):
    def create(title="Example", description="Description", status="pending"):
        resp = client.post(
            "/todos/",
            json={"title": title, "description": description, "status": status},
        )
        assert resp.status_code == 200, resp.text
        return resp.json()

    return create
