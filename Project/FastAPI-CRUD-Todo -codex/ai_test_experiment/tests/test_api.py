from sqlalchemy import select

from models.models import TodoItem


def create_todo(client, **payload):
    return client.post("/todos/", json=payload)


def test_root_endpoint(isolated_api):
    client, _ = isolated_api
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Enhanced FastAPI Todo App!"}


def test_empty_list_is_isolated_per_test_database(isolated_api):
    client, _ = isolated_api
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_uses_default_optional_values(isolated_api):
    client, _ = isolated_api
    response = create_todo(client, title="Buy milk")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Buy milk"
    assert body["description"] is None
    assert body["status"] == "pending"


def test_create_and_get_full_todo(isolated_api):
    client, _ = isolated_api
    created = create_todo(
        client,
        title="Write report",
        description="Include test evidence",
        status="doing",
    )
    assert created.status_code == 200
    todo_id = created.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": todo_id,
        "title": "Write report",
        "description": "Include test evidence",
        "status": "doing",
    }


def test_create_requires_title(isolated_api):
    client, _ = isolated_api
    response = client.post("/todos/", json={"description": "missing title"})
    assert response.status_code == 422


def test_create_rejects_null_title(isolated_api):
    client, _ = isolated_api
    response = create_todo(client, title=None)
    assert response.status_code == 422


def test_create_rejects_structurally_invalid_field_type(isolated_api):
    client, _ = isolated_api
    response = create_todo(client, title=["not", "a", "string"])
    assert response.status_code == 422


def test_pydantic_v1_coerces_integer_string_field(isolated_api):
    client, _ = isolated_api
    response = create_todo(client, title=123)
    assert response.status_code == 200
    assert response.json()["title"] == "123"


def test_read_missing_todo_returns_404(isolated_api):
    client, _ = isolated_api
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_non_integer_path_parameter_returns_422(isolated_api):
    client, _ = isolated_api
    response = client.get("/todos/not-an-integer")
    assert response.status_code == 422


def test_list_skip_and_limit_return_expected_slice(isolated_api):
    client, _ = isolated_api
    for title in ("first", "second", "third"):
        assert create_todo(client, title=title).status_code == 200

    response = client.get("/todos/?skip=1&limit=1")
    assert response.status_code == 200
    assert [todo["title"] for todo in response.json()] == ["second"]


def test_limit_zero_returns_empty_list(isolated_api):
    client, _ = isolated_api
    assert create_todo(client, title="one").status_code == 200
    response = client.get("/todos/?limit=0")
    assert response.status_code == 200
    assert response.json() == []


def test_negative_limit_is_currently_accepted_and_returns_all_rows(isolated_api):
    client, _ = isolated_api
    for title in ("one", "two"):
        assert create_todo(client, title=title).status_code == 200

    response = client.get("/todos/?limit=-1")
    assert response.status_code == 200
    assert [todo["title"] for todo in response.json()] == ["one", "two"]


def test_update_changes_only_supplied_fields(isolated_api):
    client, _ = isolated_api
    created = create_todo(
        client,
        title="old title",
        description="old description",
        status="pending",
    )
    todo_id = created.json()["id"]

    response = client.put(f"/todos/{todo_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json() == {
        "id": todo_id,
        "title": "old title",
        "description": "old description",
        "status": "done",
    }


def test_empty_update_preserves_existing_values(isolated_api):
    client, _ = isolated_api
    created = create_todo(client, title="unchanged", description="keep", status="pending")
    todo_id = created.json()["id"]

    response = client.put(f"/todos/{todo_id}", json={})
    assert response.status_code == 200
    assert response.json()["title"] == "unchanged"
    assert response.json()["description"] == "keep"
    assert response.json()["status"] == "pending"


def test_update_allows_explicit_null_optional_fields(isolated_api):
    client, _ = isolated_api
    created = create_todo(client, title="title", description="description", status="pending")
    todo_id = created.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"description": None, "status": None},
    )
    assert response.status_code == 200
    assert response.json()["description"] is None
    assert response.json()["status"] is None


def test_update_rejects_structurally_invalid_field_type(isolated_api):
    client, _ = isolated_api
    created = create_todo(client, title="title")
    todo_id = created.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"description": {"bad": "type"}})
    assert response.status_code == 422


def test_update_null_title_should_be_rejected_without_internal_error(isolated_api):
    client, session_local = isolated_api
    created = create_todo(client, title="title")
    todo_id = created.json()["id"]

    response = client.put(f"/todos/{todo_id}", json={"title": None})
    with session_local() as db:
        stored_title = db.execute(
            select(TodoItem.title).where(TodoItem.id == todo_id)
        ).scalar_one()

    assert response.status_code == 422, (
        f"expected request validation error, got {response.status_code}; "
        f"body={response.text!r}; stored_title={stored_title!r}"
    )


def test_update_missing_todo_returns_404(isolated_api):
    client, _ = isolated_api
    response = client.put("/todos/999", json={"status": "done"})
    assert response.status_code == 404


def test_delete_removes_todo_and_returns_detail(isolated_api):
    client, _ = isolated_api
    created = create_todo(client, title="remove me")
    todo_id = created.json()["id"]

    deleted = client.delete(f"/todos/{todo_id}")
    assert deleted.status_code == 200
    assert deleted.json() == {"detail": "Todo deleted"}
    assert client.get(f"/todos/{todo_id}").status_code == 404


def test_delete_missing_todo_returns_404(isolated_api):
    client, _ = isolated_api
    response = client.delete("/todos/999")
    assert response.status_code == 404

