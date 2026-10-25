"""正常 CRUD 流程与资源不存在路径的测试。"""


def test_create_todo_full_fields(client):
    r = client.post(
        "/todos/",
        json={"title": "Buy milk", "description": "2% milk", "status": "pending"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "2% milk"
    assert data["status"] == "pending"
    assert isinstance(data["id"], int)


def test_create_todo_minimal_fields(client):
    """仅提供必填 title，验证 description/status 的默认值。"""
    r = client.post("/todos/", json={"title": "Only title"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Only title"
    assert data["description"] is None
    assert data["status"] == "pending"


def test_create_then_read_by_id(client):
    r = client.post("/todos/", json={"title": "Read me"})
    todo_id = r.json()["id"]
    r2 = client.get(f"/todos/{todo_id}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Read me"


def test_id_auto_increments(client):
    ids = [client.post("/todos/", json={"title": f"t{i}"}).json()["id"] for i in range(3)]
    assert ids == [1, 2, 3]


def test_read_todo_not_found_404(client):
    r = client.get("/todos/99999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Todo not found"


def test_list_todos_returns_all_created(client, seed):
    ids = seed(3)
    r = client.get("/todos/")
    assert r.status_code == 200
    got = r.json()
    assert len(got) == 3
    assert [x["id"] for x in got] == ids


def test_update_full(client):
    todo_id = client.post("/todos/", json={"title": "old"}).json()["id"]
    r = client.put(
        f"/todos/{todo_id}",
        json={"title": "new", "description": "updated", "status": "done"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "new"
    assert data["description"] == "updated"
    assert data["status"] == "done"
    # 数据库/接口状态一致性
    r2 = client.get(f"/todos/{todo_id}")
    assert r2.json() == data


def test_update_partial_only_title(client):
    todo_id = client.post(
        "/todos/", json={"title": "keep", "description": "d", "status": "pending"}
    ).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": "changed"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "changed"
    assert data["description"] == "d"       # 未提供的字段保持不变
    assert data["status"] == "pending"


def test_update_not_found_404(client):
    r = client.put("/todos/99999", json={"title": "x"})
    assert r.status_code == 404


def test_delete_todo(client):
    todo_id = client.post("/todos/", json={"title": "to delete"}).json()["id"]
    r = client.delete(f"/todos/{todo_id}")
    assert r.status_code == 200
    assert r.json() == {"detail": "Todo deleted"}


def test_delete_then_read_404(client):
    todo_id = client.post("/todos/", json={"title": "gone"}).json()["id"]
    assert client.delete(f"/todos/{todo_id}").status_code == 200
    assert client.get(f"/todos/{todo_id}").status_code == 404


def test_delete_twice_404(client):
    todo_id = client.post("/todos/", json={"title": "once"}).json()["id"]
    assert client.delete(f"/todos/{todo_id}").status_code == 200
    assert client.delete(f"/todos/{todo_id}").status_code == 404


def test_delete_not_found_404(client):
    r = client.delete("/todos/99999")
    assert r.status_code == 404