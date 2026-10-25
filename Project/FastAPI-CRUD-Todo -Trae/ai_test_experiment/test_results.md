# 测试执行结果汇总（test_results.md）

## 1. 执行环境

- Python：3.10.21（conda env `todo_test`）
- pytest：9.1.1；pytest-cov：7.1.0；coverage：7.16.1；httpx：0.27.2（由 0.28.1 降级）
- FastAPI：0.95.2；starlette：0.27.0；SQLAlchemy：2.0.21；Pydantic：1.10.12

## 2. 执行命令

```powershell
$env:PYTHONPATH = "<项目根目录>"
python -m pytest ai_test_experiment/tests -v `
  --basetemp=ai_test_experiment/.pytest_tmp `
  --cov=main --cov=routers --cov=schemas --cov=models --cov=database `
  --cov-branch --cov-report=term-missing `
  --cov-report=html:ai_test_experiment/raw_logs/htmlcov
```

## 3. 首次运行与最终运行

- **首次运行**：38 收集；2 failed + 36 passed。
  - 2 个失败均为测试脚本缺陷（`test_list_negative_limit_ignores_limit`、`test_list_negative_skip_treated_as_zero` 缺少 `seed` fixture 参数，`NameError: name 'seed' is not defined`），属测试脚本问题，非项目缺陷。
- **另一次环境性失败**：未降级 httpx 前，`TestClient` 初始化报 `TypeError: Client.__init__() got an unexpected keyword argument 'app'`（httpx 0.28 移除了 `app` 参数与 starlette 0.27 不兼容）——测试环境问题。
- **最终运行**：38 collected；**38 passed, 0 failed, 0 error, 0 skipped**。

## 4. 覆盖率

| 指标 | 数值 | 说明 |
|---|---|---|
| 行/语句覆盖率 (line/statement) | **95.18%**（79/83） | 未覆盖 4 行：`database/database.py` L11-L15 的 `get_db` 函数体 |
| 分支覆盖率 (branch) | **100%**（8/8） | 全部命中，0 部分分支 |
| coverage.py 综合 percent_covered | 95.60% | 含分支的加权值 |
| 模块级明细 | main 100%、routers/todo 100%、models 100%、schemas 100%、database 64% | — |

未覆盖说明：`get_db` 函数体因测试通过 `dependency_overrides` 替换了依赖而未被直接调用；其等价逻辑已由测试会话工厂覆盖，属测试隔离设计的预期结果，非缺陷。

原始输出：`raw_logs/pytest_run.txt`、`raw_logs/coverage.json`、`raw_logs/htmlcov/`。

## 5. 覆盖概况（功能/接口）

- 根路由 `/`：已覆盖。
- `POST /todos/`（创建）：已覆盖（含缺 title、null title、空 body、类型强转、空/空白 title、非法 status、额外字段）。
- `GET /todos/`（列表）：已覆盖默认/组合/零/越界/负值/非整型 skip/limit。
- `GET /todos/{id}`：已覆盖存在、不存在、非整型、负数、0。
- `PUT /todos/{id}`：已覆盖全量/部分/不存在/空 body/置 null title/置 null status。
- `DELETE /todos/{id}`：已覆盖删除、删除后读取、重复删除、不存在。

## 6. 疑似缺陷

共 5 项：1 项确认缺陷（BUG-001），4 项待确认/需求不明确（BUG-002~005）。详见 defects.md。