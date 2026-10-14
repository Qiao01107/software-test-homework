# 实验一——基于 JUnit 的单元测试（Codex 独立测试）

本目录保存使用 **Codex 普通模式**独立测试 `Calculator.java` 的结果，未使用外部或自定义测试 Skills。实验根据功能需求设计用例，使用 JUnit 5 和 Maven 执行测试，识别程序缺陷并保存执行证据。本目录将用于后续人工测试、普通 Codex 测试、Codex + Skills 测试的对比；这里仅陈述本次已验证的结果。

## 目录文件

本目录无子目录。下表列出全部 5 份既有测试产物及本 README；路径均相对于本目录。README 仅作阅读入口，不属于原始测试证据。

| 文件 | 相对路径 | 用途与主要内容 | 建议重点查看 |
| --- | --- | --- | --- |
| [report.md](./report.md) | `report.md` | 中文测试报告：需求依据、测试范围、执行命令、结果统计和失败原因分析。 | 是，先看 |
| [test-cases.md](./test-cases.md) | `test-cases.md` | 12 条用例清单：输入、预期输出、实际输出及逐项结果。 | 是 |
| [surefire-report.txt](./surefire-report.txt) | `surefire-report.txt` | Maven Surefire 原始文本报告：测试计数、失败用例 Z01 的断言及堆栈。 | 是，核对失败证据 |
| [maven-test.log](./maven-test.log) | `maven-test.log` | Maven 测试完整控制台记录：编译、JUnit Platform 执行、汇总、`BUILD FAILURE` 和退出码 1。 | 是，核对执行过程 |
| [CodexCalculatorRequirementTest.java](./CodexCalculatorRequirementTest.java) | `CodexCalculatorRequirementTest.java` | JUnit 5 参数化测试源码副本：`@CsvSource` 中定义 12 组输入和需求预期值；实际执行的源码位于项目 `src/test/java/com/example/lab1/`。 | 需要审查测试设计时查看 |
| [README.md](./README.md) | `README.md` | 本目录导航和结果摘要；本次新增，不作为已有测试证据。 | 入口 |

## 测试执行情况

采用等价类划分和边界值分析：按“两个参数是否大于 0”划分输入类别，并检查 0 边界、负数及参数位置组合；用 JUnit 5 参数化测试执行。记录的 Maven 命令在项目根目录执行，使用 `-Dtest=CodexCalculatorRequirementTest` 只运行本次测试类，因此以下数字不包含项目其他测试类。

| 执行用例 | 通过 | 失败 | 错误 | 跳过 |
| ---: | ---: | ---: | ---: | ---: |
| 12 | 11 | 1 | 0 | 0 |

发现 1 处功能不符：用例 Z01 输入 `(0, 1)`，按需求应返回 `0`，实际返回 `1`。测试产生的是**断言失败**；Maven 因此报告 `BUILD FAILURE`、退出码 1，记录中没有测试运行错误。计数和失败断言可由 [Surefire 报告](./surefire-report.txt)与 [Maven 日志](./maven-test.log)核对，输入和预期值见[用例清单](./test-cases.md)。

**覆盖率：**本目录未记录覆盖率统计，也没有覆盖率结果文件；覆盖率数值无法确认。

## 建议阅读顺序

1. 阅读 [测试报告](./report.md)，了解需求、方法、实际命令及结论。
2. 查看[测试用例清单](./test-cases.md)，核对全部输入、预期值与逐项结果。
3. 查看 [Surefire 报告](./surefire-report.txt)中的 Z01 断言，再按需查阅 [Maven 日志](./maven-test.log)确认完整执行过程。
4. 如需审查测试实现，阅读 [JUnit 5 测试源码副本](./CodexCalculatorRequirementTest.java)。
