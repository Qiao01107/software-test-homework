# 干预与运行日志

| 阶段 | 现象/目的 | 处理 | 是否改动业务源码 |
|---|---|---|---|
| 环境检查 | Python 3.13.5 中未安装 FastAPI、pytest 等依赖 | 在临时虚拟环境 `C:\Users\Qiao\AppData\Local\Temp\fastapi_todo_test_venv_20261006` 安装项目依赖、pytest、pytest-cov | 否 |
| 依赖导入 | `pydantic==1.10.12` 导入 FastAPI 时因 Python 3.13 的 `ForwardRef._evaluate()` 变更失败 | 测试环境改用同一 1.10 系列的 `pydantic==1.10.24` | 否 |
| 依赖导入 | `SQLAlchemy==2.0.21` 在 Python 3.13 出现 `TypingOnly` 断言错误 | 测试环境改用同一 2.0 系列的 `SQLAlchemy==2.0.43` | 否 |
| TestClient | FastAPI/Starlette 项目依赖不自动安装 httpx | 安装测试依赖 `httpx==0.24.1` | 否 |
| 测试隔离 | 业务配置固定指向 `./todo.db` | 仅在测试 fixture 中覆盖 `get_db`，每测试使用临时 SQLite 文件；未修改数据库配置 | 否 |
| 首次运行 | 21 项收集，20 通过、1 失败 | 分析失败，确认是被测行为复现而不是测试脚本错误；未修改测试断言 | 否 |
| 最终运行 | 需要获得 statement/branch coverage | 使用同一测试集运行 `pytest-cov --cov-branch`，保留原始输出 | 否 |

测试脚本被人工或 Agent 修正次数：0。没有为提高通过率修改业务代码，也没有修改失败断言。

