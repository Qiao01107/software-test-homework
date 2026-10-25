# 过程记录（intervention_log.md）

本文件记录测试过程中的环境处理、依赖安装、测试脚本修正，以及为何修改、修改内容与修改后结果。

---

## 1. 环境探测

- 系统默认 `python`（Python 3.13.5，anaconda base）未安装 fastapi/sqlalchemy/pydantic，无法运行被测项目。
- 项目 `__pycache__` 为 `cpython-310`，提示历史运行环境为 Python 3.10。
- `conda env list` 发现 `todo_test` 环境：Python 3.10.21，已安装 fastapi 0.95.2 / sqlalchemy 2.0.21 / pydantic 1.10.12、pytest 9.1.1、httpx、pytest-cov、coverage，与 requirements.txt 完全匹配。
- **决定**：使用 `D:\CodeTools\conda_envs\todo_test\python.exe` 执行测试。业务源码零修改。

## 2. 依赖处理：降级 httpx（测试环境问题）

- **现象**：首次用 `TestClient` 建客户端报错：
  `TypeError: Client.__init__() got an unexpected keyword argument 'app'`。
- **原因**：环境内 httpx 0.28.1 移除了 `app` 快捷参数，而 fastapi 0.95.2 附带的 starlette 0.27.0 `TestClient` 仍以 `app=...` 调用 httpx.Client，版本不兼容。属**测试环境问题**，非项目缺陷。
- **处理**：`pip install "httpx==0.27.2"`（需在沙箱外执行，涉及 conda env 目录写权限）。
- **结果**：安装成功后 `TestClient` 正常初始化。

## 3. 环境处理：pytest 临时目录权限（测试环境问题）

- **现象**：所有用例 setup 阶段报
  `PermissionError: [WinError 5] 拒绝访问: 'C:\Users\Qiao\AppData\Local\Temp\pytest-of-Qiao'`。
- **原因**：pytest 默认 `tmp_path` 根目录在该系统临时路径下无法扫描/写入。
- **处理**：新增 `--basetemp=ai_test_experiment/.pytest_tmp`，将临时数据库放到项目内可写目录。
- **结果**：fixture 正常创建独立临时库。

## 4. 测试脚本修正（测试脚本问题）

- **现象**：首次运行 `2 failed`，均为
  `NameError: name 'seed' is not defined`，位于
  `test_list_negative_limit_ignores_limit`、`test_list_negative_skip_treated_as_zero`。
- **原因**：两个测试函数签名漏写 `seed` fixture 参数（`def test_...(client)`），函数体内却调用了 `seed(5)`。
- **处理**：将两处签名改为 `(client, seed)`。
- **结果**：修改后 38 项全部通过。

## 5. 隔离副作用说明（非问题）

- 导入 `main` 时其模块级 `Base.metadata.create_all(bind=engine)` 会对正式 `todo.db` 执行一次**幂等**建表（表已存在，不写入任何业务数据）。该行为属被测代码本身，未修改；正式库数据在测试过程中全程未被读写。

## 6. 总结：问题分类

| 序号 | 问题 | 分类 | 是否修复 |
|---|---|---|---|
| 1 | httpx 0.28 与 starlette 0.27 TestClient 不兼容 | 环境问题 | 是（降级 httpx） |
| 2 | 系统临时目录权限致 tmp_path 失败 | 环境问题 | 是（改 basetemp） |
| 3 | 两处测试缺 seed fixture 参数 | 测试脚本问题 | 是（修签名） |
| 4 | BUG-001 title=null → 500 | 项目缺陷 | 否（不改业务代码） |