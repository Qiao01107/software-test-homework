# 最终总结（final_summary.md）

## 0. 结论摘要

对 FastAPI-CRUD-Todo 完成了可复现的接口自动化测试：共生成 38 个测试用例，最终 38 全部通过；确认 1 个高严重度真实缺陷（PUT 将 `title` 置空导致 500 并污染数据库），另有 4 项因项目未定义规格而归类为“待确认/需求不明确”的校验缺失问题。业务源码零修改。

## 1. 实际生成测试数

38 个（分布在 4 个测试文件：test_root.py 1、test_crud.py 13、test_validation.py 13、test_list_pagination.py 11）。

## 2. pytest 实际收集测试数

38 个（collected 38 items）。

## 3. 首次运行通过/失败/错误

- 首次（含测试脚本缺陷）：**2 failed + 36 passed**，0 error、0 skipped。
- 失败为测试脚本问题（两处漏写 `seed` fixture 参数），非项目缺陷。
- 更早的环境性失败（未降级 httpx、tmp_path 权限）不计入“测试结果”，见 intervention_log.md。

## 4. 最终运行通过/失败/错误

- **38 passed，0 failed，0 error，0 skipped**。

## 5. API/功能覆盖概况

- 已覆盖：根路由、创建（含默认值/缺字段/类型/空值/非法状态）、列表分页（默认/组合/零/越界/负值/非整型）、按 ID 读取（存在/不存在/非法路径）、更新（全量/部分/不存在/空 body/置 null）、删除（删除/重复删除/不存在）。
- 主要路径与参数边界均已覆盖；含 1 个确认缺陷路径。

## 6. line coverage

**95.18%**（覆盖 79 / 语句 83）。未覆盖 4 行集中在 `database/database.py` 的 `get_db` 函数体（因测试依赖覆盖而未被直接调用，等价逻辑已被测试会话工厂覆盖）。

## 7. branch coverage

**100%**（覆盖 8 / 分支 8，0 部分分支）。

## 8. 报告的疑似缺陷数

5 项。

## 9. 缺陷分类

- 确认缺陷：1 项（BUG-001）
- 待确认/需求不明确：4 项（BUG-002 ~ BUG-005）
- 测试脚本问题 / 环境问题：0 项（已全部在测试过程中修正并记录）

## 10. 测试脚本被人工或 Agent 修正的次数

1 次（补齐两处测试函数的 `seed` fixture 参数）。另有两类环境处理不属“测试脚本修正”：httpx 降级、pytest basetemp 调整。

## 11. 新安装的测试依赖

- `httpx` 由 0.28.1 → 降级为 **0.27.2**（为兼容 starlette 0.27 的 TestClient）。
- pytest、pytest-cov、coverage 均已预装在 `todo_test` 环境，无需新装。
- 未新增任何业务依赖。

## 12. 仍未完成或无法验证的内容

- `database/database.py` 的 `get_db` 函数体（L11-L15）未被直接覆盖（被依赖覆盖替换），未做专门的单元验证。
- `status` 合法取值集合、`title` 长度/非空约束、分页参数非负约束均因项目未定义规格，只能标记“待确认”，无法验证其是否为缺陷。
- 未做安全/鉴权、并发、性能类测试（项目本身无鉴权能力，超出本次范围）。

## 13. 最重要的 3 个发现

1. **PUT 将 `title` 置空导致 500 并破坏数据（BUG-001，确认缺陷）**：`TodoUpdate.title` 允许 null，且 `exclude_unset` 把显式 null 当作“置空”，随后 `TodoOut.title`（非 Optional）响应校验失败 → 500，且数据库已写入 `title=NULL`，后续 GET 同样 500。这是客户端可控输入即可触发的服务器错误 + 数据不一致，建议优先修复（校验阶段拒绝 null，或让 `title` 在更新模型中保持必填）。
2. **输入校验普遍缺失**：`title` 无最小长度/非空校验、`status` 无枚举校验、分页负值参数未校验（`limit=-1` 会返回全集）、类型被静默强转。这些虽因规格未定义不能直接判定为缺陷，但存在明显的健壮性与数据质量风险。
3. **测试环境的可复现性陷阱**：httpx 0.28 与 fastapi 0.95.2（starlette 0.27）的 TestClient 版本不兼容，且系统临时目录权限导致 pytest `tmp_path` 失败。若不在记录中显式说明版本与环境处理，他人按 README 复现测试会失败——本实验通过降级 httpx 与改用项目内 basetemp 解决，全程未修改业务代码。

## 附：复现命令

```powershell
$env:PYTHONPATH = "<项目根目录>"
D:\CodeTools\conda_envs\todo_test\python.exe -m pytest ai_test_experiment/tests -v `
  --basetemp=ai_test_experiment/.pytest_tmp `
  --cov=main --cov=routers --cov=schemas --cov=models --cov=database `
  --cov-branch --cov-report=term-missing `
  --cov-report=html:ai_test_experiment/raw_logs/htmlcov
```