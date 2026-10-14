# Calculator.add JUnit 5 单元测试报告

## 测试对象与依据

- 项目目录：`software-testing/`
- 业务代码：`src/main/java/com/example/lab1/Calculator.java`
- 构建配置：`pom.xml`，Java 21、JUnit Jupiter 5.12.2、Maven Surefire 3.5.2。
- 功能判定标准：当且仅当 `num1 > 0` 且 `num2 > 0` 时返回 `num1 + num2`；其他输入返回 `0`。
- 测试代码：`src/test/java/com/example/lab1/CodexCalculatorRequirementTest.java`，同一份源码另存于本目录。

本次仅依据上述功能需求确定预期值，并独立阅读业务代码和 `pom.xml`。未参考其他测试代码或历史结论，未修改业务代码或 `pom.xml`。需求没有规定整数加法溢出时的结果，本次只使用不会溢出的正数之和。

## 方法和覆盖范围

采用 JUnit 5 参数化测试，共 12 次调用。用例覆盖：两个正数的求和及顺序变化；0 位于任一参数及两个参数；负数位于任一参数、与 0 组合及两个参数均为负。完整输入和期望值见 `test-cases.md`。

## 实际执行命令及结果

在工作区 `D:\School\大三\上\软测\code` 执行 `rg --files -g 'pom.xml' -g 'Calculator.java'`，定位到 `software-testing/` 下的两个目标文件。最初在工作区顶层读取目标相对路径以及执行 `git status --short` 均未成功，因为这里不是 Maven 项目根目录，也不是 Git 仓库；随后在 `software-testing/` 中成功读取 `Calculator.java` 和 `pom.xml`。未读取已有测试代码或历史报告。

在 `software-testing/` 中执行以下 PowerShell 命令，并将 Maven 的标准输出和错误输出完整写入 `maven-test.log`：

```powershell
New-Item -ItemType Directory -Path 'docs/lab1/codex' -Force | Out-Null
& mvn '-Dtest=CodexCalculatorRequirementTest' '-Dstyle.color=never' test *> 'docs/lab1/codex/maven-test.log'
$testExitCode = $LASTEXITCODE
Add-Content -LiteralPath 'docs/lab1/codex/maven-test.log' -Value "MAVEN_EXIT_CODE=$testExitCode"
exit $testExitCode
```

Maven 成功编译测试源码并使用 JUnit Platform 执行指定测试类；退出码为 **1**，原因为断言失败，构建结果为 `BUILD FAILURE`。命令通过 `-Dtest` 只执行本次新增的测试类；项目其他测试类未纳入本报告的统计。随后读取 Surefire 生成的 XML 报告，逐用例核对执行状态，得到与 Maven 控制台一致的计数。

| 指标 | 数量 |
| --- | ---: |
| 执行用例 | 12 |
| 通过 | 11 |
| 失败（断言不符） | 1 |
| 错误（测试运行异常） | 0 |
| 跳过 | 0 |

## 失败用例与可能缺陷

| 用例 | 输入 `(num1, num2)` | 期望输出 | 实际输出 | 可能原因 |
| --- | --- | ---: | ---: | --- |
| Z01 | `(0, 1)` | 0 | 1 | `Calculator.add` 中第一个参数的条件是 `num1 >= 0`，允许 0 进入求和分支；需求要求 `num1 > 0`。 |

Surefire 原始断言为 `Z01 ==> expected: <0> but was: <1>`。这表明当前实现不满足“任一整数小于或等于 0 时返回 0”的要求。按照实验约束，未修复业务代码，失败证据保持原样。

## 交付文件

- `CodexCalculatorRequirementTest.java`：本次测试源码副本；可执行文件位于项目的 `src/test/java/com/example/lab1/`。
- `test-cases.md`：12 个测试用例、预期值、实际值及结果。
- `maven-test.log`：本次 Maven 测试完整控制台日志及记录的退出码。
- `surefire-report.txt`：Surefire 对指定测试类生成的原始文本报告。
- `report.md`：本报告。
