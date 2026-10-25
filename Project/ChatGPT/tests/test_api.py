"""Independent API contract, CRUD, validation, pagination, isolation and robustness tests.

Expectations: documented CRUD feature, fields declared in Pydantic models, HTTP
contract encoded in FastAPI, and no unhandled server errors for schema-valid input.
Spec-ambiguous behaviors (blank titles, status vocabulary) are not asserted.
"""
import pytest
from sqlalchemy import select
from models.models import TodoItem


def test_root_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Welcome to the Enhanced FastAPI Todo App!"}


def test_docs_available(client):
    r = client.get("/docs")
    assert r.status_code == 200 and "swagger" in r.text.lower()


def test_openapi_available(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    data = r.json()
    assert data["openapi"] and "/todos/" in data["paths"]


def test_openapi_exposes_crud(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert {"get", "post"} <= set(paths["/todos/"])
    assert {"get", "put", "delete"} <= set(paths["/todos/{todo_id}"])


def test_empty_list(client):
    assert client.get("/todos/").json() == []


def test_create_fields_and_id(client):
    r = client.post("/todos/", json={"title":"Task","description":"Info","status":"pending"})
    assert r.status_code == 200
    assert r.json()["title"] == "Task"
    assert r.json()["description"] == "Info"
    assert r.json()["status"] == "pending"
    assert isinstance(r.json()["id"], int)


def test_create_defaults(client):
    r = client.post("/todos/", json={"title":"Task"})
    assert r.status_code == 200
    assert r.json()["description"] is None
    assert r.json()["status"] == "pending"


def test_create_explicit_null_optionals(client):
    r = client.post("/todos/", json={"title":"Task", "description":None,"status":None})
    assert r.status_code == 200
    assert r.json()["description"] is None and r.json()["status"] is None


def test_create_distinct_ids(client, create_todo):
    a, b = create_todo("A"), create_todo("B")
    assert a["id"] != b["id"]


def test_get_created(client, create_todo):
    created = create_todo("Check", "Get", "open")
    r = client.get(f"/todos/{created['id']}")
    assert r.status_code == 200 and r.json() == created


def test_list_created(client, create_todo):
    ids = [create_todo(str(i))["id"] for i in range(3)]
    r = client.get("/todos/")
    assert r.status_code == 200
    assert {item["id"] for item in r.json()} == set(ids)


def test_put_title_only(client, create_todo):
    item = create_todo("Before", "keep", "pending")
    r = client.put(f"/todos/{item['id']}", json={"title":"After"})
    assert r.status_code == 200
    assert r.json()["title"] == "After"
    assert r.json()["description"] == "keep"
    assert r.json()["status"] == "pending"


def test_put_description_only(client, create_todo):
    item = create_todo("Keep", "Before", "pending")
    r = client.put(f"/todos/{item['id']}", json={"description":"After"})
    assert r.status_code == 200
    assert r.json()["title"] == "Keep"
    assert r.json()["description"] == "After"


def test_put_status_only(client, create_todo):
    item = create_todo("Keep", "Text", "pending")
    r = client.put(f"/todos/{item['id']}", json={"status":"completed"})
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    assert r.json()["title"] == "Keep"


def test_put_all_fields(client, create_todo):
    item = create_todo("Before")
    body = {"title":"After", "description":"New", "status":"done"}
    r = client.put(f"/todos/{item['id']}", json=body)
    assert r.status_code == 200
    assert all(r.json()[key] == value for key, value in body.items())


def test_put_empty_json_noop(client, create_todo):
    item = create_todo("Stay", "Stay", "pending")
    r = client.put(f"/todos/{item['id']}", json={})
    assert r.status_code == 200 and r.json() == item


def test_put_persisted_on_requery(client, create_todo):
    item = create_todo("Before")
    client.put(f"/todos/{item['id']}", json={"title":"After"})
    assert client.get(f"/todos/{item['id']}").json()["title"] == "After"


def test_put_description_null(client, create_todo):
    item = create_todo("Keep", "Some description")
    r = client.put(f"/todos/{item['id']}", json={"description":None})
    assert r.status_code == 200 and r.json()["description"] is None


def test_put_status_null(client, create_todo):
    item = create_todo("Keep", "Notes", "active")
    r = client.put(f"/todos/{item['id']}", json={"status":None})
    assert r.status_code == 200 and r.json()["status"] is None


def test_delete_success(client, create_todo):
    item = create_todo("Delete")
    r = client.delete(f"/todos/{item['id']}")
    assert r.status_code == 200 and r.json() == {"detail": "Todo deleted"}


def test_delete_persisted(client, create_todo):
    item = create_todo("Delete")
    client.delete(f"/todos/{item['id']}")
    assert client.get(f"/todos/{item['id']}").status_code == 404
    assert client.get("/todos/").json() == []


def test_delete_other_survives(client, create_todo):
    a, b = create_todo("A"), create_todo("B")
    client.delete(f"/todos/{a['id']}")
    assert client.get(f"/todos/{b['id']}").json()["title"] == "B"


def test_get_missing_id_404(client):
    r = client.get("/todos/99999")
    assert r.status_code == 404 and r.json()["detail"] == "Todo not found"


def test_put_missing_id_404(client):
    r = client.put("/todos/99999", json={"title":"No"})
    assert r.status_code == 404 and r.json()["detail"] == "Todo not found"


def test_delete_missing_id_404(client):
    r = client.delete("/todos/99999")
    assert r.status_code == 404 and r.json()["detail"] == "Todo not found"


def test_second_delete_404(client, create_todo):
    item = create_todo("Delete twice")
    assert client.delete(f"/todos/{item['id']}").status_code == 200
    assert client.delete(f"/todos/{item['id']}").status_code == 404


def test_get_zero_id_404(client):
    assert client.get("/todos/0").status_code == 404


def test_get_negative_id_404(client):
    assert client.get("/todos/-5").status_code == 404


@pytest.mark.parametrize("wrong_id", ["abc", "1.2", "null", "1%20OR%201=1"])
def test_invalid_id_get_422(client, wrong_id):
    assert client.get(f"/todos/{wrong_id}").status_code == 422


@pytest.mark.parametrize("method", ["put", "delete"])
def test_invalid_id_mutation_422(client, method):
    r = getattr(client, method)("/todos/word", **({"json": {"title": "Y"}} if method == "put" else {}))
    assert r.status_code == 422


def test_missing_title_create_422(client):
    assert client.post("/todos/", json={"description":"No title"}).status_code == 422


def test_null_title_create_422(client):
    assert client.post("/todos/", json={"title":None}).status_code == 422


@pytest.mark.parametrize("payload", [{"title": []}, {"title": {}}, {"title": True}])
def test_create_invalid_title_type_422(client, payload):
    assert client.post("/todos/", json=payload).status_code == 422


@pytest.mark.parametrize("field", ["title", "description", "status"])
def test_create_invalid_complex_field_422(client, field):
    payload = {"title":"good", field:{"nested": "invalid"}}
    assert client.post("/todos/", json=payload).status_code == 422


@pytest.mark.parametrize("field", ["title", "description", "status"])
def test_put_invalid_complex_field_422(client, create_todo, field):
    item = create_todo("Original")
    r = client.put(f"/todos/{item['id']}", json={field: ["invalid"]})
    assert r.status_code == 422
    assert client.get(f"/todos/{item['id']}").json()["title"] == "Original"


def test_create_nonobject_422(client):
    assert client.post("/todos/", json=[{"title":"A"}]).status_code == 422


def test_create_missing_body_422(client):
    assert client.post("/todos/").status_code == 422


def test_invalid_create_has_no_side_effect(client):
    client.post("/todos/", json={"description":"No title"})
    assert client.get("/todos/").json() == []


def test_invalid_put_has_no_side_effect(client, create_todo):
    item = create_todo("Original")
    client.put(f"/todos/{item['id']}", json={"title": ["x"]})
    assert client.get(f"/todos/{item['id']}").json() == item


def test_pagination_limit(client, create_todo):
    for i in range(5): create_todo(f"item-{i}")
    r = client.get("/todos/?limit=2")
    assert r.status_code == 200 and len(r.json()) == 2


def test_pagination_skip(client, create_todo):
    items = [create_todo(f"item-{i}") for i in range(4)]
    r = client.get("/todos/?skip=2&limit=2")
    assert r.status_code == 200
    assert [i["id"] for i in r.json()] == [i["id"] for i in items[2:]]


def test_pagination_default_10(client, create_todo):
    for i in range(12): create_todo(f"item-{i}")
    r = client.get("/todos/")
    assert r.status_code == 200 and len(r.json()) == 10


def test_pagination_zero_limit(client, create_todo):
    create_todo("A")
    r = client.get("/todos/?limit=0")
    assert r.status_code == 200 and r.json() == []


def test_pagination_skip_past_end(client, create_todo):
    create_todo("A")
    r = client.get("/todos/?skip=100")
    assert r.status_code == 200 and r.json() == []


@pytest.mark.parametrize("query", ["skip=bad", "limit=bad", "skip=1.5", "limit=2.5"])
def test_pagination_bad_type_422(client, query):
    assert client.get(f"/todos/?{query}").status_code == 422


def test_unrelated_method_405(client):
    assert client.patch("/todos/123", json={"title":"new"}).status_code == 405


@pytest.mark.parametrize("text", [
    "中文任务", "Emoji ✅ 🚀", "O'Reilly; DROP TABLE todos;--", "<script>alert('x')</script>",
    "line1\nline2", " x  y ", "a" * 1024,
])
def test_title_round_trip_safely(client, create_todo, text):
    item = create_todo(text)
    r = client.get(f"/todos/{item['id']}")
    assert r.status_code == 200 and r.json()["title"] == text


def test_description_unicode_round_trip(client, create_todo):
    item = create_todo("A", "多语言 + العربية + 😀")
    assert client.get(f"/todos/{item['id']}").json()["description"] == "多语言 + العربية + 😀"


def test_stored_records_match_api(client, create_todo, db_session_factory):
    item = create_todo("Stored", "In SQLite", "pending")
    with db_session_factory() as session:
        row = session.execute(select(TodoItem).where(TodoItem.id == item["id"])).scalar_one()
        assert (row.title, row.description, row.status) == ("Stored", "In SQLite", "pending")


def test_put_changes_stored_record(client, create_todo, db_session_factory):
    item = create_todo("Before")
    client.put(f"/todos/{item['id']}", json={"title":"After"})
    with db_session_factory() as session:
        assert session.get(TodoItem, item["id"]).title == "After"


def test_delete_removes_stored_record(client, create_todo, db_session_factory):
    item = create_todo("Before")
    client.delete(f"/todos/{item['id']}")
    with db_session_factory() as session:
        assert session.get(TodoItem, item["id"]) is None


def test_deleting_all_then_creating_again(client, create_todo):
    a, b = create_todo("A"), create_todo("B")
    client.delete(f"/todos/{a['id']}")
    client.delete(f"/todos/{b['id']}")
    c = create_todo("C")
    assert len(client.get("/todos/").json()) == 1
    assert client.get(f"/todos/{c['id']}").json()["title"] == "C"


# A schema-valid UPDATE should not produce an unhandled server error. TodoUpdate
# declares title Optional[str], but TodoOut (via TodoCreate) requires a string.
# Kept intentionally as failing regression probes if the software is defective.
def test_validated_null_title_update_must_not_500(client, create_todo):
    item = create_todo("Valid")
    r = client.put(f"/todos/{item['id']}", json={"title": None})
    assert r.status_code < 500, f"valid schema input caused server error: {r.status_code}: {r.text}"


def test_null_title_update_must_not_break_subsequent_get(client, create_todo):
    item = create_todo("Valid")
    client.put(f"/todos/{item['id']}", json={"title": None})
    r = client.get(f"/todos/{item['id']}")
    assert r.status_code < 500, f"GET broken after update: {r.status_code}: {r.text}"


def test_null_title_update_must_not_break_list(client, create_todo):
    item = create_todo("Valid")
    client.put(f"/todos/{item['id']}", json={"title": None})
    r = client.get("/todos/")
    assert r.status_code < 500, f"LIST broken after update: {r.status_code}: {r.text}"
