# FastAPI-CRUD-Todo 独立软件测试实验报告

**测试对象**：用户本次上传的 `FastAPI-CRUD-Todo.zip`；本实验只依据压缩包内的源码及自带 README 分析。  
**执行日期**：2026-10-08  
**测试类型**：黑盒 HTTP/API 集成测试 + 灰盒源码/Schema 检查 + SQLite 持久化验证 + 等价类/边界值 + 输入鲁棒性回归测试。  
**测试结论**：79 个 pytest 实例中 76 通过、3 失败、0 error、0 skipped。3 个失败关联 **同一确认缺陷 D-001**；并非三个独立漏洞。限定统计的源文件语句覆盖率 83/83 (100%)，分支覆盖率 8/8 (100%)。**该覆盖率不代表无缺陷**。  
**重大环境限制**：当前安装环境不能使用源码 `requirements.txt` 指定的原始版本；本次是在较新兼容组件上执行，需在原锁定版本环境再次确认兼容性。详情见第 2 节和 `CHANGELOG.md`。

## 1. 被测系统分析（独立审查）

### 1.1 结构和技术栈

项目没有传统前端；提供由 Uvicorn 托管的 FastAPI REST 服务和 Swagger `/docs`。应用技术栈：Python、FastAPI、Pydantic、SQLAlchemy ORM、SQLite。源码依赖写明：FastAPI 0.95.2、Pydantic 1.10.12、Uvicorn 0.22.0、SQLAlchemy 2.0.21。测试工具：pytest、FastAPI TestClient (基于 httpx)、pytest-cov、coverage.py。实验执行环境的实际版本见 `environment_versions.json`。

```text
FastAPI-CRUD-Todo/
├── main.py                应用初始化、建表、挂载路由、根接口
├── database/database.py   sqlite:///./todo.db、engine、SessionLocal、get_db
├── models/models.py       TodoItem ORM 数据库结构
├── schemas/schemas.py     TodoCreate / TodoUpdate / TodoOut
├── routers/todo.py        所有 Todo CRUD 控制器
├── requirements.txt       业务依赖声明
├── README.md              项目文档
└── todo.db                压缩包自带原始 SQLite 数据库（未被测试连接）
```

数据库表 `todos(id INTEGER PRIMARY KEY, title TEXT, description TEXT, status TEXT)`。`id` 作为主键；`title`、`description`、`status` 都未设置 `nullable=False` 或校验约束。`Base.metadata.create_all(bind=engine)` 在导入 `main.py` 时建表，连接 URL 为 **相对当前工作目录** 的 `./todo.db`；这是保证数据库隔离需要特别关注的细节。

### 1.2 接口路由

| 路由 | HTTP | 作用 | 源码正常成功状态 | 关键检查 |
|---|---|---|---|---|
| `/` | GET | 欢迎文本 | 200 | 返回 JSON |
| `/todos/` | POST | 新建 Todo | 200 | 请求 Schema；`add/commit/refresh`；ID、默认值 |
| `/todos/` | GET | 列表 | 200 | `skip=0`、`limit=10`；offset/limit |
| `/todos/{todo_id}` | GET | 单项读取 | 200 | `id:int`；不存在 404 |
| `/todos/{todo_id}` | PUT | 部分字段更新 | 200 | `exclude_unset=True`；不存在 404 |
| `/todos/{todo_id}` | DELETE | 删除 | 200 | 提交数据库；不存在 404 |
| `/docs`, `/openapi.json` | GET | API 文档和 Schema | 200 | 路由可发现性 |

### 1.3 Schema 及重要业务规则

- `TodoCreate`：`title: str` 必填；`description: Optional[str] = None`；`status: Optional[str] = "pending"`。没有字段长度、空串或状态枚举限制。
- `TodoUpdate`：全部字段 `Optional[str] = None`，PUT 更新时使用 `todo.dict(exclude_unset=True)`，即区分“缺少键”和“显式传入 null”。
- `TodoOut`：继承 `TodoCreate` 并添加 `id: int`，因此输出 **title 必须是字符串**。
- **核心不变量风险**：`TodoUpdate.title` 允许显式传入 null，ORM 的 `title` 列允许存 null，但 `TodoOut.title` 不允许 null；更新后会触发响应校验失败。
- 未实现认证、审计、状态流转和业务规则校验；这些不能在无产品需求依据时直接认定为功能缺陷。

## 2. 测试环境、隔离与可追溯性

- **原件隔离**：上传 ZIP 解压至 `original/FastAPI-CRUD-Todo/`。从该文件夹复制**未修改的五个 Python 业务源码**到 `working/app/`。只在 `working/app/` 运行服务代码，避免业务代码使用相对路径连接原始 `todo.db`。
- **数据库隔离**：测试 fixture 每个用例用 `tmp_path/isolated_test.sqlite3` 创建全新 SQLite 文件；用 FastAPI `dependency_overrides[get_db]` 临时替换数据库依赖，并在每个用例结束后清理 override、释放 SQLAlchemy engine。此 override 只存在于测试进程，没有更改任何业务源码。
- **原始数据库保护证据**：原件 `todo.db` SHA-256 是 `3d8e828e06a427d6c73c15c609bcf6245c176441809bd751174996e53c713828`，与直接从上传 ZIP 流读取的该文件哈希完全一致。`cmp` 验证测试用的全部五个源码文件与解压原件一致。
- **原始 ZIP 校验**：SHA-256 `e8736c90e8e44445aa459dd4ac63edb201e4468857f3290b38e5c7566747a0cd`；可与 `source_manifest.json` 核验。
- **依赖限制**：当前 Python 3.13.5；项目声明 FastAPI 0.95.2/Pydantic 1.10.12/SQLAlchemy 2.0.21/Uvicorn 0.22.0。尝试在 venv 安装兼容原版本组合失败，原因是安装源 DNS 无法解析（见 `logs/install_dependencies.log`），不是应用的安装逻辑故障。随后改用系统已有 FastAPI 0.128.2、Pydantic 2.13.5、SQLAlchemy 2.0.50、httpx 0.28.1，pytest 9.0.2；未修改业务代码。这属于**测试环境与原始依赖不一致的限制**，不应隐瞒。
- **环境告警**：Pydantic v2 对 `orm_mode` 及 `.dict()` 提出兼容性弃用告警；这些属于环境版本相关提示，未计为已确认业务缺陷。本次 89 条 warning 大多由这些提示的重复发生造成。

## 3. 测试设计和实际覆盖面

针对 REST API 和数据库持久化，编写 `tests/test_api.py` 与 `tests/test_database.py`，共收集 **79 个独立 pytest 参数化实例**。主要测试维度：

1. 根路径、Swagger 与 OpenAPI 可用性/路由声明。
2. 创建、读取、列表、更新、删除的正常链路及其数据库持久化证据。
3. title 必填、缺少 JSON、非对象 JSON、数值/列表/字典/布尔等输入类型校验。
4. 404/422/405，重复删除、不存在 ID、零/负 ID、非法 ID。
5. 分页默认值、skip、limit、零 limit、超大 skip 和非整数参数。
6. 更新部分字段、空字典、显式 null 的可选字段；已知问题的三个回归探针。
7. 中文、表情、引号、类 SQL 注入文本、HTML 标签、换行、空格、长标题的**存取一致性**（并非完整安全审计）。
8. SQLite 表结构、主键、数据库 session 关闭行为、原始记录未污染。

为了不以主观假设制造“失败”，**空标题是否允许、状态是否必须属于枚举、分页负数是否必须被拒绝**只做了非断言式表征，结果另存 `unspecified_behavior.json`，其业务规则有待产品确认。

## 4. 执行结果与覆盖率

| 指标 | 首次测试 | 最终测试 |
|---|---:|---:|
| pytest collected | 79 | 79 |
| 实际执行 | 79 | 79 |
| passed | 76 | 76 |
| failed | 3 | 3 |
| error | 0 | 0 |
| skipped | 0 | 0 |
| pytest exit code | 1 | 1（确认回归测试保持失败） |
| coverage | 首次未采集 | 83/83 statement；8/8 branch |
| 覆盖率 | — | statement 100.00%；branch 100.00%；coverage 综合 100% |

初次 `pytest --collect-only` 与初次真实运行已分别保存 `logs/pytest_collect_initial.log`、`logs/pytest_initial.log` 和 `reports/junit_initial.xml`。最终运行见 `logs/pytest_final.log`、`reports/junit_final.xml`、`reports/coverage.xml` 和可浏览的 `reports/htmlcov/index.html`。

覆盖范围只包括 `main.py`、`database/database.py`、`models/models.py`、`routers/todo.py`、`schemas/schemas.py`。项目逻辑较短；100% 覆盖率不代表完整的异常、权限、并发、性能、负载或端到端浏览器覆盖。

## 5. 缺陷报告

### D-001（确认的软件缺陷 / 高严重度 P1）

**标题**：PUT 允许把 Todo 标题持久化为 NULL，随后更新响应、单条查询和列表查询均出现 HTTP 500。  
**涉及接口**：`PUT /todos/{todo_id}`、`GET /todos/{todo_id}`、`GET /todos/`。  
**前提**：独立干净 SQLite 数据库。

**复现步骤**：

1. `POST /todos/`，JSON `{"title":"original", "description":"keep"}`，成功返回 `200` 和 `id=1`（测试数据库）。
2. `GET /todos/1`，正常返回 200。
3. `PUT /todos/1`，JSON `{"title":null}`。
4. 再次调用 `GET /todos/1` 和 `GET /todos/`。
5. 用原生 sqlite3 查询表中该行，确认真实持久化值。

**实际结果**：步骤 3 `500 Internal Server Error`，步骤 4 两种 GET 同样为 500；数据库查询显示 `(1, NULL, 'keep', 'pending')`。启用测试客户端异常传播后，三个接口均抛出 `fastapi.exceptions.ResponseValidationError`，报告 `title` 响应字段不是字符串。完整异常和 HTTP 请求响应取证见 `targeted_reproduction.json`。

**预期结果及依据**：`TodoUpdate.title: Optional[str]` 将 null 作为允许输入，因此合法 Schema 输入不应导致 500。设计可允许 null 且调整响应/业务模型，或拒绝 null 并返回 4xx、保持旧值，或实现其他明确的业务规则；不强制指定修复方案。至少必须保证请求不会造成不受控的 5xx、破坏后续查询可用性。既有 Schema 同时声明 `TodoOut.title: str`，提供了响应契约依据。

**根因（基于源码和复现）**：`routers/todo.py` 行 36–39 直接以 `exclude_unset=True` 将显式 null 写入 `TodoItem.title` 并 `commit()`，而 `models/models.py` 行 8 的列允许 NULL；`schemas/schemas.py` 中 `TodoOut` 继承了非空的 `TodoCreate.title: str`。因此写入成功后响应校验报错，后续查询读取到该条坏记录也报错。**先提交数据库、后生成响应**，所以客户端见到 500 并不意味着事务自动回滚。

**缺陷分类**：输入约束不一致 / 数据完整性 / 服务端未处理错误 / CRUD 持久化缺陷。  
**严重程度**：高（P1）：单次合法 Schema 输入可使列表 API 持续不可用，持久化异常数据直到纠正。  
**可复现性**：已在临时 SQLite 中独立复现，3 个自动化回归测试稳定失败。受前述组件版本偏差限制，需要在原锁定环境复核确认其跨版本表现。  
**关联失败测试**：`test_validated_null_title_update_must_not_500`、`test_null_title_update_must_not_break_subsequent_get`、`test_null_title_update_must_not_break_list`。

### S-001（待确认 / 需求规格不明确）：分页负数和上限

**接口**：`GET /todos/?limit=-1` / `?skip=-1` / `?limit=100000`。  
**输入与结果**：在 12 条数据下，`limit=-1` 返回 200 和 12 条；`skip=-1` 返回 200 和默认 limit 的 10 条；`limit=100000` 返回 200 和 12 条。见 `unspecified_behavior.json`。  
**期望结果及依据**：常见 API 规范会约束 `skip >= 0`、`1 <= limit <= max_limit`，但当前源码及 README 未明确业务要求。  
**分类**：待确认设计风险，而非正式失败；如果列表可能大规模增长，负数 `limit` 或无上界 `limit` 存在资源消耗风险。  
**严重程度**：低至中，取决于接口规模/可访问性。**未列为确认缺陷**。

### S-002（需求/规格不明确）：标题内容与状态值

**接口**：`POST /todos/`。  
**输入**：`{"title":""}`、`{"title":"  "}`、`{"title":"x","status":"some-made-up-status"}`。  
**结果**：均返回 200 并原样保存。  
**期望结果及依据**：如果产品要求非空白标题或有限状态枚举，应加入明确约束；源码和 README 没有这类规范，不能据此判定错误。  
**分类**：需求/规格不明确。**不计为失败**。

### DOC-001（确认文档偏差 / 低严重度）

README 的 “Project Structure” 将 `database.py`、`models.py`、`schemas.py` 画在项目根目录，但实际源码位于 `database/`、`models/`、`schemas/` 子目录。属于文档准确性问题，**不是这次三个失败用例的原因**。

### 环境与脚本问题的分类结果

| 类别 | 结果与证据 |
|---|---|
| 确认的软件缺陷 | D-001，一项根因、三处接口表现 |
| 待确认问题 | S-001，分页参数缺少非负/上界约束的风险 |
| 需求/规格不明确 | S-002，空标题与状态自由取值；S-001 也涉及规格缺失 |
| 测试脚本问题 | 初次测试收集与执行未发现需要修正的测试脚本错误，**修正次数为 0** |
| 测试环境问题 | 隔离 venv 安装原版依赖失败；改用已安装的新版依赖，并记录偏差、完整错误日志 |
| 文档质量偏差 | DOC-001，README 目录说明与实际不一致 |

## 6. 修正审计与文件完整性

在记录的首次 pytest 运行之后，**没有修改、跳过、删除或 xfail 任何失败测试**。最终运行仅增加 coverage/JUnit 输出，并额外执行隔离复现与非断言式规格表征脚本。尝试安装依赖失败后选择现有环境是**环境适配**；由于未安装原版本，该限制写入报告。完整事件记录见 `reports/CHANGELOG.md`、`logs/install_dependencies.log`。

测试源码只位于 `tests/`，诊断脚本位于 `tools/`。应用源码 `working/app` 与原始 ZIP 相同；无产品修复和业务重构。

## 7. 局限、结论和后续建议

- **结论**：正常 CRUD、分页及若干边界输入整体工作；D-001 是会污染数据库并导致读接口持续 500 的高影响错误。不能用 76/79 通过或 100% 覆盖率掩盖它。
- **验证缺口**：因离线下载失败，未能在原项目锁定的 Python/依赖组合执行一次对照测试；也未做并发压力、安全授权审计、真实服务器网络部署或生产数据迁移测试。因此结果是当前实际环境中的有证据缺陷，不应表述为“所有环境均已验证”。
- **下一步（仅建议，未修改源码）**：先明确 null 标题的业务预期，针对 `TodoUpdate`/ORM/输出一致性修复并新增回归；同时明确分页范围、状态词汇和标题空白规则，再在与原 `requirements.txt` 完全一致的环境重跑相同测试。

## 8. 交付材料和重现命令

```text
independent_audit/
├── REPORT.md, CHANGELOG.md, metrics.json, source_manifest.json
├── environment_versions.json, pip_freeze_full.txt
├── working/app/               应用源码副本（不含原始 todo.db）
├── tests/conftest.py          每用例的独立 SQLite 和依赖覆盖
├── tests/test_api.py          HTTP CRUD / 校验 / 边界 / 缺陷探针
├── tests/test_database.py     数据库与会话生命周期检查
├── tools/reproduce_and_characterize.py
├── tools/characterize_unspecified_inputs.py
├── pytest.ini, run_tests.sh
├── logs/                      收集、首次、最终、安装失败、诊断日志
└── reports/                   JUnit XML、coverage XML/HTML、目标取证
```

**Linux / macOS，先安装依赖后从交付根目录执行：**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r working/app/requirements.txt 'httpx==0.24.1' pytest pytest-cov
bash run_tests.sh
```

**Windows PowerShell（推荐 Python 3.10）：**

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\working\app\requirements.txt 'httpx==0.24.1' pytest pytest-cov
cd .\working\app
$env:PYTHONPATH = (Get-Location).Path
python -m pytest ..\..\tests -c ..\..\pytest.ini --cov=main --cov=database --cov=models --cov=routers --cov=schemas --cov-branch --cov-report=term-missing
```

预期当前未修复应用仍有三个针对 D-001 的失败用例，故 pytest **exit code=1 属于预期的缺陷检测结果**，不应通过篡改业务源码或删除失败用例使其变为 0。报告中 100% 代码覆盖率是本次 Python 3.13 的实际执行记录；在 Python 3.10/pinned 版本上需重新测量，不能保证完全相同。
