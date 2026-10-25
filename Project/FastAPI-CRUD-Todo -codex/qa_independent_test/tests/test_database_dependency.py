import pytest

import database.database as database_module


def test_get_db_closes_session_after_consumption(monkeypatch: pytest.MonkeyPatch) -> None:
    class SessionStub:
        closed = False

        def close(self) -> None:
            self.closed = True

    session = SessionStub()
    monkeypatch.setattr(database_module, "SessionLocal", lambda: session)
    dependency = database_module.get_db()

    assert next(dependency) is session
    with pytest.raises(StopIteration):
        next(dependency)
    assert session.closed is True
