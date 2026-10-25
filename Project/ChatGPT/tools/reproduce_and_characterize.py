"""Standalone, repeatable defect reproduction using original app handlers.

This utility uses a newly-created temporary SQLite file (NOT todo.db),
then captures raw SQLite rows, HTTP responses, and validation exceptions.
The app source code is never altered.
"""
import json
import sqlite3
import tempfile
import traceback
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, get_db
from main import app


def run():
    with tempfile.TemporaryDirectory(prefix="todo_repro_") as tmp:
        dbfile = Path(tmp) / "repro.sqlite3"
        engine = create_engine(f"sqlite:///{dbfile}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

        def override():
            session = Session()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_db] = override
        try:
            with TestClient(app, raise_server_exceptions=False) as client:
                created = client.post("/todos/", json={"title": "original", "description": "keep"})
                obj = created.json()
                url = f"/todos/{obj['id']}"
                before = client.get(url)
                bad_update = client.put(url, json={"title": None})
                after_get = client.get(url)
                after_list = client.get("/todos/")
            with sqlite3.connect(dbfile) as conn:
                rows = conn.execute("SELECT id, title, description, status FROM todos ORDER BY id").fetchall()
            with TestClient(app, raise_server_exceptions=True) as client:
                exception_info = {}
                for name, verb, endpoint, payload in [
                    ("update", "PUT", url, {"title":None}),
                    ("get", "GET", url, None),
                    ("list", "GET", "/todos/", None),
                ]:
                    try:
                        client.request(verb, endpoint, json=payload)
                        exception_info[name] = {"raised": False}
                    except Exception as e:
                        exception_info[name] = {
                            "raised": True,
                            "exception_type": type(e).__name__,
                            "exception_message": str(e)[:2000],
                            "traceback_excerpt": "".join(traceback.format_exception(type(e), e, e.__traceback__))[-2500:],
                        }
            result = {
                "source": "Only uploaded ZIP unmodified Python sources in working/app",
                "sqlite": "unique temporary test file, deleted after capture",
                "input": {"initial_post": {"title":"original", "description":"keep"}, "update": {"title":None}},
                "post": {"status":created.status_code,"json":obj},
                "before_get": {"status":before.status_code,"json":before.json()},
                "put_null_title": {"status":bad_update.status_code,"body":bad_update.text},
                "after_get": {"status":after_get.status_code,"body":after_get.text},
                "after_list": {"status":after_list.status_code,"body":after_list.text},
                "sqlite_rows_after_failed_update": rows,
                "raised_exceptions": exception_info,
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        finally:
            app.dependency_overrides.clear()
            engine.dispose()


if __name__ == "__main__":
    run()
