"""根路由测试。"""


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Welcome to the Enhanced FastAPI Todo App!"}