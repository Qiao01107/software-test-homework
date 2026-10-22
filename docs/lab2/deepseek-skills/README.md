# 实验二 JUnit 5 白盒测试 —— DeepSeek V4 Pro + Skills 组

本目录为 **DeepSeek V4 Pro + software-testing-lab Skill 独立实验组** 的实验二交付物。
覆盖标准：语句覆盖 / 判定覆盖 / 条件覆盖 / 条件-判定覆盖。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `test_report.md` | 完整中文测试报告（含环境、需求分析、执行结果、覆盖分析、缺陷记录、总结） |
| `test_cases.md` | 测试用例与条件/判定覆盖矩阵（含短路求值 T/F/NE 与四种覆盖标准的满足依据） |
| `maven-test.log` | Maven 原始测试日志（Run 2，UTF-8 规范化） |
| `surefire-report.txt` | Surefire 结果摘要（`target/surefire-reports` 原样复制） |
| `surefire-report.xml` | Surefire 原始 XML（`target/surefire-reports` 原样复制） |
| `skill-loading-evidence.md` | Skill 实际读取记录（文件清单、SHA256、要点摘录与应用映射） |
| `README.md` | 本文件 |

测试源码：`src/test/java/com/example/lab2/DeepSeekSkillLab2CoverageTest.java`

## 复现方式

```bash
cd D:\School\3\up\软测\code\software-testing
mvn "-Dtest=DeepSeekSkillLab2CoverageTest" test
```

预期结果：`Tests run: 4, Failures: 0, Errors: 0, Skipped: 0`，`BUILD SUCCESS`。

## 环境

- OS：Windows 11（amd64）
- Java：Oracle JDK 21.0.11（`D:\CodeTools\Java\jdk-21.0.11`）
- Maven：Apache Maven 3.9.16（`D:\CodeTools\Apache\apache-maven-3.9.16`）
- JUnit Jupiter 5.12.2；maven-surefire-plugin 3.5.2；maven-compiler-plugin 3.13.0（release 21）

## 独立性说明

- 未读取 `docs/lab2/codex/`、其他组测试类或历史结果。
- 未修改原始 `Calculator.java` 与 `pom.xml`（SHA256 见 `test_report.md`）。
- 仅新增本组测试类与 `docs/lab2/deepseek-skills/` 下的交付物。
