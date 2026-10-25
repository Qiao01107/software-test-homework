from typing import Any

from fastapi.testclient import TestClient


def assert_todo_shape(payload: dict[str, Any]) -> None:
    assert set(payload) == {"id", "title", "description", "status"}
    assert isinstance(payload["id"], int)
    assert isinstance(payload["title"], str)
    assert payload["description"] is None or isinstance(payload["description"], str)
    assert payload["status"] is None or isinstance(payload["status"], str)


def create_todo(client: TestClient, title: str = "Buy milk") -> dict[str, Any]:
    response = client.post("/todos/", json={"title": title, "description": "groceries"})
    assert response.status_code == 200
    payload = response.json()
    assert_todo_shape(payload)
    return payload


def test_root_health_message_and_json_header(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"message": "Welcome to the Enhanced FastAPI Todo App!"}


def test_create_applies_default_status_and_returns_contract(client: TestClient) -> None:
    payload = create_todo(client)

    assert payload["title"] == "Buy milk"
    assert payload["description"] == "groceries"
    assert payload["status"] == "pending"


def test_crud_lifecycle_and_delete_idempotency(client: TestClient) -> None:
    created = create_todo(client)
    todo_id = created["id"]

    listed = client.get("/todos/")
    assert listed.status_code == 200
    assert listed.headers["content-type"].startswith("application/json")
    assert [item["id"] for item in listed.json()] == [todo_id]

    fetched = client.get(f"/todos/{todo_id}")
    assert fetched.status_code == 200
    assert fetched.json() == created

    updated = client.put(
        f"/todos/{todo_id}",
        json={"description": "weekly groceries", "status": "done"},
    )
    assert updated.status_code == 200
    assert updated.json() == {
        "id": todo_id,
        "title": "Buy milk",
        "description": "weekly groceries",
        "status": "done",
    }

    deleted = client.delete(f"/todos/{todo_id}")
    assert deleted.status_code == 200
    assert deleted.json() == {"detail": "Todo deleted"}
    assert client.get(f"/todos/{todo_id}").status_code == 404
    assert client.delete(f"/todos/{todo_id}").status_code == 404


def test_update_preserves_unset_fields(client: TestClient) -> None:
    created = create_todo(client, title="Original")

    response = client.put(f"/todos/{created['id']}", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["title"] == "Original"
    assert response.json()["description"] == "groceries"
    assert response.json()["status"] == "done"


def test_validation_errors_are_422_for_missing_or_wrongly_typed_input(
    client: TestClient,
) -> None:
    missing_title = client.post("/todos/", json={"description": "missing title"})
    wrong_id = client.get("/todos/not-an-integer")

    assert missing_title.status_code == 422
    assert wrong_id.status_code == 422
    assert isinstance(missing_title.json()["detail"], list)
    assert isinstance(wrong_id.json()["detail"], list)


def test_missing_todo_returns_consistent_404_contract(client: TestClient) -> None:
    response = client.get("/todos/999")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"detail": "Todo not found"}


def test_update_missing_todo_returns_consistent_404_contract(client: TestClient) -> None:
    response = client.put("/todos/999", json={"status": "done"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_pagination_limit_and_skip_are_applied(client: TestClient) -> None:
    for title in ("A", "B", "C"):
        create_todo(client, title=title)

    first_page = client.get("/todos/", params={"skip": 0, "limit": 2})
    second_page = client.get("/todos/", params={"skip": 2, "limit": 2})

    assert first_page.status_code == 200
    assert [item["title"] for item in first_page.json()] == ["A", "B"]
    assert [item["title"] for item in second_page.json()] == ["C"]


def test_empty_list_is_returned_for_empty_database(client: TestClient) -> None:
    response = client.get("/todos/")

    assert response.status_code == 200
    assert response.json() == []
