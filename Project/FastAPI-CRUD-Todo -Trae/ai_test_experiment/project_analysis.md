# 项目分析（project_analysis.md）

## 1. 概述

本项目 `FastAPI-CRUD-Todo` 是一个用于演示 CRUD 操作的简单 FastAPI + SQLAlchemy + SQLite 待办事项应用。

## 2. 技术栈

| 项目 | 版本（requirements.txt 指定） | 实际运行环境 |
|---|---|---|
| Python | 3.7+（README 声明） | 3.10.21（conda env `todo_test`） |
| FastAPI | 0.95.2 | 0.95.2 |
| Pydantic | 1.10.12 | 1.10.12 |
| Uvicorn | 0.22.0 | 0.22.0 |
| SQLAlchemy | 2.0.21 | 2.0.21 |
| (starlette) | — | 0.27.0 |

数据库：SQLite，SQLAlchemy ORM 方式。

## 3. 目录结构

```
FastAPI-CRUD-Todo/
├── main.py                # 应用入口：建表 + 挂载路由
├── database/
│   └── database.py        # engine / SessionLocal / Base / get_db()
├── models/
│   └── models.py          # SQLAlchemy 模型 TodoItem
├── schemas/
│   └── schemas.py         # Pydantic 模型 TodoCreate / TodoUpdate / TodoOut
├── routers/
│   └── todo.py            # CRUD 路由
├── requirements.txt
├── README.md
└── todo.db                # SQLite 数据文件
```

## 4. 数据库方式

- 连接串：`sqlite:///./todo.db`（[database.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/database/database.py)）。
- `engine` / `SessionLocal` / `Base` 在模块导入时创建，属模块级单例。
- `get_db()` 为 FastAPI 依赖，yield 一个会话并在 finally 中关闭。
- `main.py` 在模块导入时执行 `Base.metadata.create_all(bind=engine)` 建表。

### 数据模型 `TODOItem`（表 `todos`）

| 字段 | 类型 | 约束 |
|---|---|---|
| id | Integer | 主键、自增、索引 |
| title | String | 索引；无 nullable=False（默认可空）、无长度校验 |
| description | String | 索引；可空 |
| status | String | 索引；可空 |

## 5. Pydantic Schema

**TodoCreate**：`title: str`（必填）；`description: Optional[str] = None`；`status: Optional[str] = "pending"`。

**TodoUpdate**：`title/description/status` 均为 `Optional[str] = None`（全部可选，用于部分更新）。

**TodoOut**：继承 TodoCreate 并新增 `id: int`；`Config.orm_mode = True`。

> 关键点：`TodoOut.title` 继承自 `TodoCreate.title`，是非 Optional 的 `str`。这为后续 PUT 置空 title 的缺陷埋下伏笔。

## 6. 主要 API 清单

路由前缀 `/todos`，标签 `Todos`；另有根路由。

| 方法 | 路径 | 处理函数 | 输入 | 成功响应 | 异常路径 |
|---|---|---|---|---|---|
| GET | `/` | `read_root` | 无 | `{"message": "..."}` | — |
| POST | `/todos/` | `create_todo` | body: TodoCreate | 201 语义但实际 200，TodoOut | title 缺失/为 null → 422 |
| GET | `/todos/` | `read_todos` | query: skip=0, limit=10 | 200，`List[TodoOut]` | skip/limit 非 int → 422 |
| GET | `/todos/{todo_id}` | `read_todo` | path: int | 200，TodoOut | id 非 int → 422；不存在 → 404 |
| PUT | `/todos/{todo_id}` | `update_todo` | path: int；body: TodoUpdate | 200，TodoOut | id 非 int → 422；不存在 → 404；title=null → 500（缺陷）|
| DELETE | `/todos/{todo_id}` | `delete_todo` | path: int | 200，`{"detail":"Todo deleted"}` | id 非 int → 422；不存在 → 404 |

## 7. 识别到的行为特征与风险点（供测试覆盖）

1. **无输入校验层**：title 无 min_length/非空校验，status 无枚举/白名单。
2. **Pydantic v1 非严格模式**：`str` 字段会被 int/float/bool 静默强转为字符串。
3. **UPDATE 的部分更新语义**：`exclude_unset=True`，显式传 `null` 会被当作“置空”，而 `TodoOut.title` 非 Optional，导致响应模型校验失败 → 500。
4. **skip/limit 未做非负/上限校验**：SQLite 中 `LIMIT -1` 表示无上限、`OFFSET` 负值按 0 处理。
5. **删除接口幂等性缺失**：重复删除返回 404（是否合理取决于规格）。
6. **响应状态码**：POST 返回 200 而非 REST 惯例的 201（规格未定义，不影响功能）。

## 8. 测试隔离控制点

见 [conftest.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/ai_test_experiment/tests/conftest.py)：通过 `app.dependency_overrides[get_db]` 将路由依赖替换为指向每个测试独立临时 SQLite 文件的会话工厂，从而不污染正式 `todo.db`。