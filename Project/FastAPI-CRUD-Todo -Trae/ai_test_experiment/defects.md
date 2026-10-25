# 疑似缺陷记录（defects.md）

说明：仅依据实际运行结果与源码判定，“不确定是否符合预期”的行为一律归为“待确认/需求不明确”，不自动升格为缺陷。

---

## BUG-001

- **缺陷编号**：BUG-001
- **标题**：PUT 更新将 `title` 显式置为 null 时接口返回 500，并污染数据库数据
- **涉及接口/文件**：`PUT /todos/{todo_id}`；[routers/todo.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/routers/todo.py) `update_todo`；[schemas/schemas.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/schemas/schemas.py) `TodoUpdate`/`TodoOut`
- **前置条件**：存在一条待办（id 已知）
- **重现步骤**：
  1. `POST /todos/ {"title":"before"}` → 得到 id
  2. `PUT /todos/{id} {"title": null}`
  3. `GET /todos/{id}`
- **实际结果**：
  - 步骤 2 返回 `500 Internal Server Error`
  - 数据库中该行 `title` 已被写成 `NULL`
  - 步骤 3 返回 `500 Internal Server Error`
- **期望结果及其依据**：`title` 是 `TodoCreate` 的必填 `str` 字段，显式传 null 应被 422 拒绝（与 `POST {"title": null}` 的 422 行为一致），或至少不应导致服务器 500 与数据库脏数据。
- **根因**：`TodoUpdate.title` 为 `Optional[str]=None`，`todo.dict(exclude_unset=True)` 会把“显式传 null”当作“已设置”，执行 `setattr(db_todo, "title", None)`。而 `title` 数据库列可空，写入 NULL 成功；随后 `response_model=TodoOut`（`title: str` 非 Optional）校验失败，抛出 ResponseValidationError → 500。
- **严重程度建议**：高（客户端可控输入导致服务器错误 + 数据不一致）
- **支撑证据**：
  - 探针输出：`PUT title=None -> 500 Internal Server Error`、`GET after -> 500`、`DB row title value = None`
  - 测试 `test_update_title_null_causes_500`（PASS，断言 500）
  - `test_update_status_null_ok` 证明 status（Optional）置 null 不报错，形成对照
- **最终分类**：**确认缺陷**

---

## BUG-002

- **缺陷编号**：BUG-002
- **标题**：`status` 字段无枚举/白名单校验，任意字符串可写入
- **涉及接口/文件**：`POST /todos/`、`PUT /todos/{id}`；[schemas/schemas.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/schemas/schemas.py) `TodoCreate.status`
- **前置条件**：无
- **重现步骤**：`POST /todos/ {"title":"x","status":"banana"}`
- **实际结果**：返回 200，`status` 被存为 `banana`
- **期望结果及其依据**：项目仅示意默认值 `pending`，README 未定义合法取值集合，故不能确定 `banana` 非法；需与产品确认是否需要枚举（如 pending/in-progress/done）。
- **严重程度建议**：中（取决于业务规则）
- **支撑证据**：测试 `test_post_arbitrary_status_accepted`（PASS，断言 200 且 status="banana"）
- **最终分类**：**待确认 / 需求不明确**

---

## BUG-003

- **缺陷编号**：BUG-003
- **标题**：`title` 缺少非空/最小长度校验，空字符串与纯空白可写入
- **涉及接口/文件**：`POST /todos/`；[schemas/schemas.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/schemas/schemas.py) `TodoCreate.title`
- **前置条件**：无
- **重现步骤**：`POST /todos/ {"title":""}` 或 `{"title":"   "}`
- **实际结果**：返回 200，创建空标题待办
- **期望结果及其依据**：`title` 为必填字段，通常应拒绝空/纯空白输入；但 README 未明确约束，不能完全判定为缺陷。
- **严重程度建议**：中
- **支撑证据**：测试 `test_post_empty_string_title_accepted`、`test_post_whitespace_title_accepted`（均 PASS）
- **最终分类**：**待确认 / 需求不明确**

---

## BUG-004

- **缺陷编号**：BUG-004
- **标题**：入参类型被 Pydantic 静默强转（int/bool → str），而非拒绝
- **涉及接口/文件**：`POST /todos/`；[schemas/schemas.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/schemas/schemas.py)
- **前置条件**：无
- **重现步骤**：`POST /todos/ {"title":123}`（或 `status: 123`）
- **实际结果**：返回 200，`title` 被转换为 `"123"`
- **期望结果及其依据**：非字符串类型的 title 是否应拒绝取决于规格；Pydantic v1 非严格模式默认强转，属于框架默认行为。
- **严重程度建议**：低
- **支撑证据**：测试 `test_post_title_int_coerced_to_string`、`test_post_status_int_coerced`（均 PASS）
- **最终分类**：**待确认 / 需求不明确（框架默认行为）**

---

## BUG-005

- **缺陷编号**：BUG-005
- **标题**：`skip`/`limit` 缺少非负与上限校验，负值可导致分页失效/全集返回
- **涉及接口/文件**：`GET /todos/`；[routers/todo.py](file:///d:/School/大三/上/软测/小组/Project/FastAPI-CRUD-Todo%20-Trae/routers/todo.py) `read_todos`
- **前置条件**：数据库存在多条记录
- **重现步骤**：`GET /todos/?limit=-1`；`GET /todos/?skip=-1`
- **实际结果**：
  - `limit=-1` → 返回全部记录（SQLite `LIMIT -1` 无上限）
  - `skip=-1` → 返回全部记录（SQLite `OFFSET` 负值按 0 处理）
- **期望结果及其依据**：分页参数通常要求非负；负值应被 422 拒绝或至少不导致“取全部”。但项目未定义分页约束，属不确定项。
- **严重程度建议**：低
- **支撑证据**：测试 `test_list_negative_limit_ignores_limit`、`test_list_negative_skip_treated_as_zero`（均 PASS，断言返回 5 条）
- **最终分类**：**待确认 / 需求不明确**

---

## 汇总

| 编号 | 标题 | 分类 | 严重程度 |
|---|---|---|---|
| BUG-001 | PUT title=null → 500 且污染数据 | 确认缺陷 | 高 |
| BUG-002 | status 无枚举校验 | 待确认/需求不明确 | 中 |
| BUG-003 | title 无长度/非空校验 | 待确认/需求不明确 | 中 |
| BUG-004 | 类型静默强转 | 待确认/需求不明确 | 低 |
| BUG-005 | skip/limit 负值未校验 | 待确认/需求不明确 | 低 |

- 确认缺陷：1 项
- 待确认/需求不明确：4 项
- 测试脚本问题 / 环境问题：0 项（详见 intervention_log.md，均已修正）