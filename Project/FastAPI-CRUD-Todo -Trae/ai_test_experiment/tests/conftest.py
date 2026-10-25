"""pytest 公共 fixture 与路径配置。

隔离策略说明：
- 项目的数据库引擎在 database/database.py 模块导入时即固定为 sqlite:///./todo.db。
- 为不污染正式 todo.db，测试通过 fastapi 的 dependency_overrides 机制，
  把路由依赖的 get_db 替换为指向每个测试独立的临时 SQLite 文件数据库。
- 该替换不修改任何业务源码，仅在测试进程内生效。
- 注：导入 main 时其模块级 Base.metadata.create_all(bind=engine) 仍会对
  正式 todo.db 执行一次幂等的建表（表已存在故无副作用、不写入业务数据），
  这是被测代码的模块级行为，未做改动。
"""

import os
import sys

# 将项目根目录加入 sys.path，以便 import main / routers / schemas / models / database
HERE = os.path.dirname(os.path.abspath(__file__))          # .../ai_test_experiment/tests
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))       # 项目根目录
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database.database import Base, get_db
from main import app


@pytest.fixture()
def client(tmp_path):
    """为每个测试提供独立的临时数据库与 TestClient。

    raise_server_exceptions=False：使未被捕获的服务器异常以 500 响应返回，
    便于在测试中断言“应返回 500”的场景（如响应模型校验失败）。
    """
    db_file = tmp_path / "test_todo.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


@pytest.fixture()
def seed(client):
    """创建 n 个待办并返回其 id 列表。"""
    def _seed(n):
        ids = []
        for i in range(n):
            r = client.post(
                "/todos/",
                json={"title": f"todo-{i}", "description": f"desc-{i}", "status": "pending"},
            )
            assert r.status_code == 200, r.text
            ids.append(r.json()["id"])
        return ids

    return _seed