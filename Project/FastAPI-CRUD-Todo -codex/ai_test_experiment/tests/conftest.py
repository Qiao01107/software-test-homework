from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.database import Base, get_db
from main import app


@pytest.fixture
def isolated_api(tmp_path) -> Generator[tuple[TestClient, sessionmaker[Session]], None, None]:
    """Provide a fresh file-backed SQLite database for each test function."""
    database_url = f"sqlite:///{tmp_path / 'test_todo.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            yield client, testing_session_local
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

