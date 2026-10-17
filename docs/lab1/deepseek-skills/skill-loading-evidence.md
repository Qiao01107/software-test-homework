# Skill 实际读取证据（software-testing-lab）

## 加载方式声明
- 本次采用 **绝对路径直接读取文件** 的方式使用 Skill，通过 `read` 工具把 Skill 的 Markdown 文件完整读入工作上下文。
- **不是** Harness 原生 `skill()` 工具注册成功（该 Skill 不在本会话已注册 Skill 目录中；本会话目录仅含 `diagnose-windows-sandbox-acl`、`office-docx`、`office-pptx`、`office-xlsx`）。
- 读取过程为只读，未修改 `software-testing-lab` 的任何文件。

## 本轮实际读取的文件
| 文件 | 绝对路径 | 内容 |
| --- | --- | --- |
| Skill 主文件 | `D:\School\大三\上\软测\skills\software-testing-lab\SKILL.md` | 95 行，完整读取 |
| 报告模板 | `D:\School\大三\上\软测\skills\software-testing-lab\references\report-template.md` | 58 行，完整读取 |
| 多组对比规则 | `D:\School\大三\上\软测\skills\software-testing-lab\references\comparison-rubric.md` | 28 行，完整读取 |

## 同时读取的被测项目文件
| 文件 | 绝对路径 |
| --- | --- |
| 被测源码 | `D:\School\大三\上\软测\code\software-testing\src\main\java\com\example\lab1\Calculator.java` |
| 构建配置 | `D:\School\大三\上\软测\code\software-testing\pom.xml` |

## 采用的执行规范（摘要）
- 任务模式：`execute`（真实运行测试）。
- 业务源码只读，不修改 `Calculator.java`；只新增本组测试与报告。
- 期望值由功能需求推导，不以程序实际输出为正确结果。
- 测试失败与构建/环境失败分开统计；覆盖率描述不混淆。
- 独立测试类名：`DeepSeekSkillCalculatorTest`，Maven 单类筛选 `-Dtest=DeepSeekSkillCalculatorTest`，不掺入其他组测试。
