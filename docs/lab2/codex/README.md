# Lab2 Codex 独立白盒测试交付说明

## 文件用途

- `test_report.md`：中文测试报告，包含源码控制流、短路逻辑、四种覆盖标准、执行环境、结果和结论。
- `test_cases.md`：逐条测试用例、实际条件取值、判定结果、预期推导、实际输出及覆盖集合。
- `maven-test.log`：最终一次限定测试类执行的 Maven 原始控制台日志（标准输出与错误输出合并）。
- `surefire-report.txt`：Maven Surefire 生成的可读摘要副本。
- `surefire-report.xml`：Maven Surefire 生成的原始 XML 报告副本，包含测试类限定属性、每个测试方法及其实际输出。
- `../../../src/test/java/com/example/lab2/CodexLab2CoverageTest.java`：本次新增的 JUnit 5 测试源码（实际源码位于项目 `src/test` 目录，不在本报告目录内）。

## 复现方式

在 PowerShell 中执行：

```powershell
Set-Location 'D:\School\3\up\软测\code\software-testing'
mvn --no-transfer-progress "-Dstyle.color=never" "-Dtest=CodexLab2CoverageTest" test
```

命令只执行 `CodexLab2CoverageTest`。本次实际退出码为 0，结果为：测试 3、通过 3、失败 0、错误 0、跳过 0。

若要重新保存控制台日志，可执行：

```powershell
mvn --no-transfer-progress "-Dstyle.color=never" "-Dtest=CodexLab2CoverageTest" test 2>&1 |
    Tee-Object -FilePath 'docs/lab2/codex/maven-test.log'
```

复现后，Surefire 会在 `target/surefire-reports/` 中重新生成对应报告。当前交付目录中的 TXT/XML 是 2026-10-19 21:37:44（Asia/Shanghai）这次实际运行后复制的证据。

## 结果摘要

- 语句覆盖：满足，TC01+TC03。
- 判定覆盖：满足，TC01+TC03。
- 条件覆盖：满足，TC01+TC02+TC03。
- 条件/判定覆盖：满足，TC01+TC02+TC03。
- 未使用覆盖率工具，因此没有声称工具实测覆盖率百分比。
- 未发现失败用例；未修改 `Calculator.java` 或 `pom.xml`。
