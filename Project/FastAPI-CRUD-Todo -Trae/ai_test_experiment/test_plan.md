# 测试方案（test_plan.md）

## 1. 测试目标与策略

在**不修改业务源码**的前提下，对 FastAPI-CRUD-Todo 进行可复现的接口自动化测试，覆盖正常 CRUD、输入校验、边界值、异常路径、状态一致性，并识别真实缺陷。

- 测试框架：pytest + FastAPI `TestClient`（httpx 作为传输）。
- 数据库隔离：每个测试使用独立的临时 SQLite 文件（`tmp_path`），通过 `dependency_overrides` 替换 `get_db`。
- 覆盖率：pytest-cov 统计行/分支覆盖率。

## 2. 测试隔离与可重复性设计

| 项 | 做法 |
|---|---|
| 数据隔离 | fixture `client` 为每个测试创建独立 `test.db`，测试结束销毁；正式 `todo.db` 不被写入 |
| 依赖替换 | `app.dependency_overrides[get_db]` 替换为测试会话工厂 |
| 可重复执行 | 每个用例自建初始数据（`seed` fixture），不依赖执行顺序 |
| 服务器异常暴露 | `TestClient(raise_server_exceptions=False)`，便于断言 500 |

## 3. 测试点清单

### 3.1 根路由
- GET `/` 返回欢迎消息。

### 3.2 正常 CRUD 流程
- 创建（全字段 / 仅必填字段，默认值验证）
- 按 ID 读取
- 列表返回全部已建项（顺序、数量）
- 全量更新、部分更新（未提供字段保持不变）
- 删除；删除后读取 404；重复删除 404
- ID 自增连续性
- 创建/更新/删除后的接口-数据库状态一致性

### 3.3 输入验证与异常输入
- POST 缺 title → 422
- POST title=null → 422
- POST 空 body → 422
- POST title 为 int → 记录强转行为（非 422）
- POST 空字符串 / 纯空白 title → 记录被接受行为
- POST status 任意字符串 / int → 记录行为
- POST 额外字段 → 被忽略
- PUT 空 body → 空更新（无变化）
- PUT title=null → 记录 500 缺陷
- PUT status=null（Optional）→ 正常 200（对比）

### 3.4 路径参数非法 / 资源不存在
- GET/其他 `todo_id` 非 int → 422
- 负数、0、不存在 ID → 404
- PUT / DELETE 不存在 → 404

### 3.5 skip/limit 分页与边界
- 默认 limit；skip+limit 组合
- limit=0；skip 超出范围 → 空列表
- limit > 记录数 → 返回全部
- skip/limit 为负 → 记录行为（limit=-1 返回全部、skip=-1 按 0 处理）
- skip/limit 非 int → 422

## 4. 关注的其他风险
- 类型静默强转（Pydantic v1）
- 缺字段校验（title 空值、status 非法值）
- 负值分页参数导致的数据全集泄漏
- 更新置空导致的 500 与数据库不一致

## 5. 覆盖率统计范围
`--cov=main --cov=routers --cov=schemas --cov=models --cov=database`，`--cov-branch`，输出 term-missing 与 html。

## 6. 判定边界（不作为缺陷的项）
- 测试脚本自身错误、测试环境问题、需求未明不确定的行为：单独归类，不自动判定为项目缺陷。