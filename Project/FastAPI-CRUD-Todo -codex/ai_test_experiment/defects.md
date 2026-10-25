# 缺陷与异常记录

## D-001：更新接口接受 null 标题后返回 500，并已提交非法状态

- 涉及接口/文件：`PUT /todos/{todo_id}`；`routers/todo.py:31-40`；`schemas/schemas.py` 中 `TodoUpdate.title` 与 `TodoOut.title` 的定义。
- 前置条件：隔离测试数据库中存在 `title="title"` 的 Todo。
- 重现步骤：
  1. `POST /todos/`，JSON 为 `{"title":"title"}`，得到 ID 1。
  2. `PUT /todos/1`，JSON 为 `{"title":null}`。
  3. 查询测试数据库中的 ID 1。
- 实际结果：HTTP 500，响应体 `Internal Server Error`；数据库查询显示该行 `title` 已为 `NULL`。
- 期望结果及依据：请求应在进入更新/提交前返回 422，或项目明确规定 null 语义并保证合法响应；不能产生未处理的 500，也不能让输出模型要求非空的 `title` 被持久化为 null。`TodoOut.title` 是必填 `str`，因此现状与自身响应契约冲突。
- 严重程度建议：中（单个输入即可触发 500，并造成后续数据状态不符合输出模型；影响面集中在显式 null 更新）。
- 支撑证据：`raw_logs/first_run.txt` 与 `raw_logs/final_run.txt` 中同名测试失败；失败断言同时报告 `got 500`、`body='Internal Server Error'`、`stored_title=None`。
- 最终分类：确认缺陷。

## D-002：负 limit 未被拒绝，SQLite 将其表现为返回全部记录

- 涉及接口/文件：`GET /todos/?limit=-1`；`routers/todo.py:20-22`。
- 前置条件：隔离数据库中创建两条 Todo。
- 重现步骤：发送 `GET /todos/?limit=-1`。
- 实际结果：HTTP 200，返回两条记录；测试 `test_negative_limit_is_currently_accepted_and_returns_all_rows` 通过。
- 期望结果及依据：通常分页参数应限制为非负整数，负 limit 应返回 422；但当前 README 没有明确分页边界，源码也没有声明 `ge=0` 约束。
- 严重程度建议：低到中（调用方输入错误时可能绕过预期分页，数据量增大时影响响应大小）。
- 支撑证据：`raw_logs/final_run.txt` 中该测试通过；`read_todos` 仅声明 `int` 默认值，没有范围校验。
- 最终分类：待确认（需要产品/API 规格确认负分页参数的预期）。

## 非缺陷环境事项

项目锁定的 Pydantic 1.10.12 与 SQLAlchemy 2.0.21 在本机 Python 3.13.5 中无法导入运行；这是测试环境/依赖兼容问题，不计入 API 缺陷。使用同一大版本的兼容补丁版本后完成测试，详情见 `intervention_log.md`。

## 需求不明确事项

- `title`/`description`/`status` 没有长度或非空约束，空字符串当前会按字符串接受；README 未定义是否应拒绝，因此没有将其判为确认缺陷。
- Pydantic 1.x 会将 JSON 整数 `123` 强制转换为字符串 `"123"`；这是当前依赖的实际语义，是否需要严格类型需规格确认。

