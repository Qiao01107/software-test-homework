# Independent FastAPI-CRUD-Todo Test Reproduction Package

## 阅读顺序

1. `reports/REPORT.md` — 独立源码分析、方法、初次/最终指标、缺陷 D-001、全部约束。
2. `reports/CHANGELOG.md` — 环境/脚本修正审计。
3. `reports/targeted_reproduction.json` — 真实 HTTP 500 与 SQLite 写入 NULL 的复现证据。
4. `logs/pytest_initial.log` 与 `logs/pytest_final.log` — 完整 pytest 日志；JUnit XML 在 `reports/`。
5. `reports/htmlcov/index.html` — 可视化覆盖率；原始覆盖率数据为 `reports/coverage.xml` 和 `reports/coverage.sqlite3`。
6. `tests/` — 79 个 pytest 用例（包含三个未删除的失败缺陷探针），`tools/` — 复现与非断言式规格表征。

### 重要说明

- 未修改上传项目任何业务 Python 源码。`working/app` 是独立工作副本。
- 不包含用户原始 `todo.db`：仅记录哈希，绝不在其上运行测试。
- 初始/最终均为 76 passed、3 failed；覆盖率 83/83 statement、8/8 branch。
- 三个失败反映同一个根因，**不是 3 个不同软件缺陷**。
- 运行环境（Python 3.13、FastAPI 0.128 等）不完全符合原 requirements，原锁定依赖因为网络问题无法安装。请在 Python 3.10 + 原 requirements 环境重测以消除该局限。
- 如需复现，先安装合适依赖，Linux/macOS 执行 `bash run_tests.sh`；Windows 使用报告中 PowerShell 命令。
