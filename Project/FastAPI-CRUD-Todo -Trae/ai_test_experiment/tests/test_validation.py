"""输入验证、类型处理与字段边界测试。

其中部分用例用于“记录实际行为”而非断言理想行为，具体是否为缺陷在 defects.md 中判定。
"""


def test_post_missing_title_422(client):
    r = client.post("/todos/", json={"description": "no title"})
    assert r.status_code == 422


def test_post_null_title_422(client):
    """title 为必填 str，显式传 null 应被 422 拒绝。"""
    r = client.post("/todos/", json={"title": None})
    assert r.status_code == 422


def test_post_empty_body_422(client):
    r = client.post("/todos/", json={})
    assert r.status_code == 422


def test_post_title_int_coerced_to_string(client):
    """pydantic v1 默认将 int 强制转换为 str（非严格模式），记录该行为。"""
    r = client.post("/todos/", json={"title": 123})
    assert r.status_code == 200
    # 实际被静默转换为字符串 "123"
    assert r.json()["title"] == "123"


def test_post_empty_string_title_accepted(client):
    """title 无 min_length 校验，空字符串被接受。记录该行为。"""
    r = client.post("/todos/", json={"title": ""})
    assert r.status_code == 200
    assert r.json()["title"] == ""


def test_post_whitespace_title_accepted(client):
    """仅空白 title 亦被接受。记录该行为。"""
    r = client.post("/todos/", json={"title": "   "})
    assert r.status_code == 200
    assert r.json()["title"] == "   "


def test_post_arbitrary_status_accepted(client):
    """status 无枚举/合法值校验，任意字符串被接受。记录该行为。"""
    r = client.post("/todos/", json={"title": "x", "status": "banana"})
    assert r.status_code == 200
    assert r.json()["status"] == "banana"


def test_post_status_int_coerced(client):
    r = client.post("/todos/", json={"title": "x", "status": 123})
    assert r.status_code == 200
    assert r.json()["status"] == "123"


def test_post_extra_field_ignored(client):
    """pydantic v1 默认忽略额外字段。"""
    r = client.post("/todos/", json={"title": "x", "foo": "bar"})
    assert r.status_code == 200
    assert "foo" not in r.json()


def test_update_empty_body_noop(client):
    """"PUT {}" 三个字段均可选，空体为合法的空更新，返回原对象不变。"""
    todo_id = client.post(
        "/todos/", json={"title": "t", "description": "d", "status": "pending"}
    ).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "t"
    assert data["description"] == "d"
    assert data["status"] == "pending"


def test_update_title_null_causes_500(client):
    """核心缺陷：PUT title=null 将 title 置为 NULL，随后响应模型 TodoOut.title
    （非 Optional 的 str）校验失败，接口返回 500。"""
    todo_id = client.post("/todos/", json={"title": "before"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": None})
    assert r.status_code == 500


def test_update_status_null_ok(client):
    """status 为 Optional[str]，PUT status=null 被接受并置为 null（与 title=null 形成对比）。"""
    todo_id = client.post("/todos/", json={"title": "s"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"status": None})
    assert r.status_code == 200
    assert r.json()["status"] is None