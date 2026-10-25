# 项目与接口分析

## 分析范围与依据

分析对象是工作区中的 FastAPI-CRUD-Todo 项目。结论依据 `README.md`、`requirements.txt`、`main.py`、`database/database.py`、`models/models.py`、`schemas/schemas.py` 和 `routers/todo.py` 的源码，以及对现有 `todo.db` 的只读检查。

## 技术栈与结构

- Python FastAPI 0.95.2，Pydantic 1.10.x，SQLAlchemy 2.0.x，SQLite，Uvicorn。
- `main.py` 创建 FastAPI 应用，在导入时执行 `Base.metadata.create_all(bind=engine)`，挂载 `/todos` 路由，并提供 `/` 欢迎接口。
- `database/database.py` 使用 `sqlite:///./todo.db`，通过 `SessionLocal` 和 `get_db()` 为请求提供会话。
- `models/models.py` 定义 `todos` 表：`id` 主键，`title`、`description`、`status` 为字符串列。
- `schemas/schemas.py` 定义创建、部分更新和输出模型。Pydantic 默认允许部分字符串类型强制转换；未设置长度或非空约束。
- `routers/todo.py` 实现 CRUD，所有业务路由都以 `/todos/` 为前缀。

现有数据库表名为 `todos`，只读检查发现已有两条记录；本实验不使用、不清理、不写入该数据库。

## 接口清单

| 方法和路径 | 输入 | 成功响应 | 异常路径 |
|---|---|---|---|
| GET `/` | 无 | 200，固定欢迎消息 | 未发现业务异常路径 |
| POST `/todos/` | JSON `title` 必填字符串；`description` 可选字符串/null；`status` 可选字符串，默认 `pending` | 200，`TodoOut`：`id/title/description/status` | 请求体字段缺失、null/结构不匹配时 422；数据库提交异常未显式处理 |
| GET `/todos/` | 查询参数 `skip` 默认 0，`limit` 默认 10 | 200，TodoOut 数组 | 非整数查询参数 422；未声明非负范围 |
| GET `/todos/{todo_id}` | 整数路径参数 | 200，TodoOut | 非整数路径参数 422；不存在 404 `Todo not found` |
| PUT `/todos/{todo_id}` | JSON `TodoUpdate`：三个字段均可选且默认 null；使用 `exclude_unset` 部分更新 | 200，更新后的 TodoOut | 非法请求体 422；不存在 404；显式 `title: null` 可通过输入模型，但会导致持久化空值与响应模型冲突，实验复现为 500 |
| DELETE `/todos/{todo_id}` | 整数路径参数 | 200，`{"detail":"Todo deleted"}` | 非整数路径参数 422；不存在 404 |

## 已识别的风险

1. `TodoUpdate.title` 可接收显式 null，但 `TodoOut.title` 不可为 null；更新顺序是先提交数据库再做响应校验，可能出现 500 和已污染状态。
2. `skip`/`limit` 未使用 `Query(ge=0)` 等范围约束；SQLite 对负 limit 的处理可能使其退化为“不限量”。
3. 字符串没有最小长度约束，空标题会被接受；README 未给出非空规格，因此仅记录为需求待确认。
4. 数据库提交和查询异常没有统一的业务错误处理；本次未人为制造数据库故障。

