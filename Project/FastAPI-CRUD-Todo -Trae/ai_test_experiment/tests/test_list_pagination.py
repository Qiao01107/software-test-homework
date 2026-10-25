"""列表分页 skip/limit 与非法路径参数测试。"""


def test_get_non_int_id_422(client):
    r = client.get("/todos/abc")
    assert r.status_code == 422


def test_get_negative_id_404(client):
    r = client.get("/todos/-1")
    assert r.status_code == 404


def test_get_zero_id_404(client):
    r = client.get("/todos/0")
    assert r.status_code == 404


def test_list_default_limit(client, seed):
    # 默认 limit=10，少于 10 条时返回全部
    seed(4)
    r = client.get("/todos/")
    assert r.status_code == 200
    assert len(r.json()) == 4


def test_list_skip_and_limit(client, seed):
    seed(5)
    r = client.get("/todos/?skip=1&limit=2")
    assert r.status_code == 200
    got = r.json()
    assert len(got) == 2
    assert [x["id"] for x in got] == [2, 3]


def test_list_limit_zero(client, seed):
    seed(3)
    r = client.get("/todos/?limit=0")
    assert r.status_code == 200
    assert r.json() == []


def test_list_skip_beyond_range(client, seed):
    seed(2)
    r = client.get("/todos/?skip=100&limit=10")
    assert r.status_code == 200
    assert r.json() == []


def test_list_negative_limit_ignores_limit(client, seed):
    """SQLite 中 LIMIT -1 表示“无上限”，返回全部记录（limit 校验缺失）。记录该行为。"""
    seed(5)
    r = client.get("/todos/?limit=-1")
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_list_negative_skip_treated_as_zero(client, seed):
    """SQLite 中 OFFSET 负值按 0 处理，返回全部（skip 校验缺失）。记录该行为。"""
    seed(5)
    r = client.get("/todos/?skip=-1&limit=10")
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_list_non_int_skip_422(client):
    r = client.get("/todos/?skip=abc")
    assert r.status_code == 422


def test_list_non_int_limit_422(client):
    r = client.get("/todos/?limit=abc")
    assert r.status_code == 422


def test_list_limit_more_than_count(client, seed):
    seed(3)
    r = client.get("/todos/?limit=100")
    assert r.status_code == 200
    assert len(r.json()) == 3