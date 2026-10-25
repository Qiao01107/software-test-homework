# 测试执行结果

## 执行环境

- OS/平台：Windows，pytest 报告平台 `win32`
- Python：3.13.5
- 运行环境：临时虚拟环境 `C:\Users\Qiao\AppData\Local\Temp\fastapi_todo_test_venv_20261006`
- 关键版本：FastAPI 0.95.2、Starlette 0.27.0、Pydantic 1.10.24、SQLAlchemy 2.0.43、httpx 0.24.1、pytest 9.1.1、pytest-cov 7.1.0、coverage 7.16.2
- 完整安装快照：[raw_logs/test_environment_pip_freeze.txt](raw_logs/test_environment_pip_freeze.txt)

## 首次运行

命令：

```text
<temporary-venv>\Scripts\python.exe -m pytest -c ai_test_experiment\pytest.ini ai_test_experiment\tests
```

结果：收集 21 项；20 passed，1 failed，0 error，0 skipped。失败为 `test_update_null_title_should_be_rejected_without_internal_error`，实际响应 500，数据库 title 为 `NULL`。

原始输出：[raw_logs/first_run.txt](raw_logs/first_run.txt)

## 最终运行

命令：

```text
<temporary-venv>\Scripts\python.exe -m pytest -c ai_test_experiment\pytest.ini ai_test_experiment\tests --cov=main --cov=routers.todo --cov=schemas.schemas --cov=models.models --cov=database.database --cov-report=term-missing --cov-branch
```

结果：收集 21 项；20 passed，1 failed，0 error，0 skipped，1 个 Starlette deprecation warning。失败与首次运行相同，未修正业务或失败测试断言。

原始输出：[raw_logs/final_run.txt](raw_logs/final_run.txt)

## 覆盖率

最终 pytest-cov 输出：

- Statement/line coverage：总计 83 statements 中覆盖 79，`96%`。
- Branch coverage：总计 8 个可测分支，覆盖 8 个，`100%`；`routers/todo.py` 分支为 8/8。
- `database/database.py` 的原始 `get_db()` 生成器行 11–15 未执行，因为测试按设计覆盖了该依赖以隔离业务数据库。

## 功能结果概览

根端点、创建默认值/完整值、按 ID 查询、列表切片、limit=0、部分更新、空更新、可选 null、删除后 404、404/422 异常路径均获得预期结果。Pydantic 1.x 将整数标题转换为字符串的行为也被实测记录。显式更新 `title: null` 是唯一失败且可复现的项目行为问题。

