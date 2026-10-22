# Skill 实际加载证据（software-testing-lab）

## 1. 加载方式

- **加载方式**：本次按用户要求采用「直接读取 Skill 指令文件」方式，通过绝对路径实际读取 Skill 目录下的文件内容，未通过 Harness 原生 `skill()` 工具注册。
- **Skill 根目录**（用户指定路径）：`D:\School\大三\上\软测\skills\software-testing-lab`
  - 注：该中文路径在文件系统上实际为 `D:\School\3\up\软测\skills\software-testing-lab`（`大三`=`3`、`上`=`up`），已用 glob 定位确认。
- **task_mode**：`execute`（设计 + 实现 + 真实运行测试，未虚构结果）。
- **lab_id / group_id**：`lab2` / `deepseek-skills`。

## 2. 实际读取的文件清单（含 SHA256）

| 文件（绝对路径） | 大小/读取 | SHA256 |
| --- | --- | --- |
| `D:\School\3\up\软测\skills\software-testing-lab\SKILL.md` | 95 行，已全文读取 | `78A6E93E0B564A6F39AA745324595B5CE227AB1EBED160AFF0C769D0890B3222` |
| `D:\School\3\up\软测\skills\software-testing-lab\references\report-template.md` | 58 行，已全文读取 | `AC741AF972AA1BAB0753A47F6DBBCCCB78ECC2FDB0E4B0CF8EB0776619E1BE49` |
| `D:\School\3\up\软测\skills\software-testing-lab\references\comparison-rubric.md` | 28 行，已全文读取 | `CDE7E03B69FE669BA1DA1D59F6FDD9A6B3C25BC707B23F9FF3CE0170BB367618` |

（哈希由 `Get-FileHash -Algorithm SHA256` 在 2026-10-20 计算得到。）

## 3. 读取内容要点摘录（证明并非仅“知道有 Skill”）

### SKILL.md 关键条款（已按其执行）

- 工作模式：`execute`（默认，需真正运行）/ `design-only` / `review` / `regression` —— 本次选择 **execute**。
- “**绝不能将程序实际行为直接当作正确结果**”——本次期望输出由人工按代码语义逐句推导，作为断言 oracle。
- 独立性与变更边界：“默认**只读业务源码**”“只新增或修改本实验组的测试、必要的测试配置和报告”“不得读取其他组的测试代码、报告、运行日志或缺陷清单”。
- 白盒要求：“语句覆盖、判定/分支覆盖、条件覆盖、条件-判定覆盖”。
- 短路求值：“对 `&&`、`||` 的短路求值要区分‘逻辑上可推断’与‘运行时实际被求值’；无法执行的条件不应虚报为已覆盖”。
- 真实执行：“`execute` 模式**必须尝试实际运行**”“运行 0 个测试不得报告为有效测试成功”“生成报告不能代替实际执行”。
- 覆盖率纪律：“不得将其直接宣称为教材中的条件覆盖、MC/DC 或路径覆盖”——本次**未使用覆盖率工具，未虚构百分比**，改用条件真值表证明。
- 交付：“按 `references/report-template.md` 选择适用章节”。

### report-template.md 关键条款（已按其组织报告）

- 第 1~8 节结构：实验基本信息 / 环境与范围 / 需求分析与测试设计 / 执行结果 / 覆盖分析 / 失败诊断与缺陷记录 / 复现步骤和证据 / 总结与限制。
- “实际执行 0 个测试不得记为有效测试成功”——本次实测 4 条，>0。

### comparison-rubric.md 关键条款（已按其执行隔离）

- “C 组须保留该次运行实际加载 `software-testing-lab` 的证据，单有 Skill 文件或调用文字不算加载”——本文件即证据。
- “盲测完成前不读取其他组结果”——本次未读取 `docs/lab2/codex/` 等任何其他组产物。

## 4. 本组对 Skill 的具体应用（映射）

| Skill 要求 | 本次执行情况 |
| --- | --- |
| execute 模式真实运行 | 通过 Maven 实际运行 2 次，均 BUILD SUCCESS，4/0/0/0 |
| 只读业务源码、不改业务代码 | 未修改 `Calculator.java`、`pom.xml`（哈希不变） |
| 区分 T/F/NE 短路 | 覆盖矩阵明确标记 C2、C4 的 NE，且 NE 不计入条件覆盖 |
| 不虚构覆盖率 | 未启用 JaCoCo，未宣称工具实测百分比；用真值表证明四种覆盖 |
| 失败与环境失败分开统计 | 0 失败、0 错误；沙箱 ACL 属环境授权问题，与测试结果分开记录 |
| 报告结构 | 按 report-template.md 8 节组织 `test_report.md` |

## 5. 结论

`software-testing-lab` Skill 在本次实验中**实际被读取并使用**（直接文件读取方式，非 Harness `skill()` 注册），其工作流、独立性与变更边界、短路求值、真实执行与证据、报告结构等要求均已落实到测试设计与执行全过程。
