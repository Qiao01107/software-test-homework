# 软件测试实验一 —— 独立 JUnit 5 单元测试报告（DeepSeek V4 Pro + Skills 组）

## 1. 实验基本信息
- 实验编号/名称：实验一（lab1）—— `Calculator.add` 单元测试
- 测试组及方式：DeepSeek V4 Pro + `software-testing-lab` Skill（组别 `deepseek-skills`）
- 测试目标与版本：`com.example.lab1.Calculator#add(int, int)`（发放源码，未做任何修改）
- 实验目的：独立判断 `Calculator.java` 是否满足给定功能需求
- 约束和独立性说明：
  - 不参考人工 JUnit、普通 Codex、Codex + Skills、ChatGPT 的已有测试结果；
  - 不阅读已有 `CalculatorTest.java`、`CodexCalculatorRequirementTest.java` 及 `docs/lab1/` 下其他组的报告/日志；
  - 未修改 `Calculator.java`、`pom.xml` 及 `software-testing-lab` 的任何文件；
  - 使用独立测试类 `DeepSeekSkillCalculatorTest.java`，未覆盖任何已有测试文件。

## 2. 环境与范围
- OS：Windows 11（amd64，version 10.0）
- 语言/运行时：Java 21.0.11（Oracle Corporation，`D:\CodeTools\Java\jdk-21.0.11`）
- 构建工具：Apache Maven 3.9.16（`D:\CodeTools\Apache\apache-maven-3.9.16`）
- 测试框架：JUnit 5（`org.junit.jupiter:junit-jupiter:5.12.2`，JUnit Platform 1.12.2）
- 运行插件：maven-surefire-plugin 3.5.2（自动检测 JUnitPlatformProvider）
- 编译插件：maven-compiler-plugin 3.13.0（release 21）
- 被测路径与功能：`src/main/java/com/example/lab1/Calculator.java` 的 `add(int num1, int num2)`
- 源码版本标识：未获取 git commit（未运行 git 命令）；以发放源码文件内容为准，见附录“源码快照”
- 环境准备/变更记录：
  - 新增测试类 `src/test/java/com/example/lab1/DeepSeekSkillCalculatorTest.java`
  - 由于会话工作区根目录 Windows 沙箱 ACL 初始化失败（`SetNamedSecurityInfoW failed (Win32 5): grantWrite(...)`），Maven 命令通过 Harness 单次受控授权（`danger-full-access`）执行，共 2 次授权（环境检查 1 次、执行测试 1 次）。**未修改任何目录 ACL，未运行权限修复脚本，未授予持续/全局权限。**

## 3. 需求分析与测试设计
功能需求（用户提供，无答案）：
- R1：两个整数都大于 0 时，返回两者之和。
- R2：只要任意一个整数小于或等于 0，就返回 0。

测试方法：黑盒等价类划分 + 边界值分析。
- 有效等价类 EC1：`num1 > 0 且 num2 > 0` → 返回 `num1 + num2`
- 无效等价类 EC2：`num1 <= 0 或 num2 <= 0` → 返回 0
- 边界点：`0`（“>0”与“<=0”的分界），`1`（>0 的紧邻上界），`-1`（<=0 的紧邻下界）

共设计 9 条用例（详见 `test_cases.md`）。

需求-用例追踪：
| 需求ID | 业务规则 | 输入范围/边界 | 对应用例ID |
| --- | --- | --- | --- |
| R1 | 两个都 > 0 → 返回和 | (1,1)、(3,5)、(1234,5678) | TC01–TC03 |
| R2 | 任一 <= 0 → 返回 0 | num1=0 / num2=0 / 双0 / 单负 / 双负 | TC04–TC09 |

## 4. 执行结果
- 执行状态：已执行
- 运行 ID：`RUN-20261016-182518`（依据 Maven `Finished at: 2026-10-16T18:25:18+08:00`）
- 工作目录：`D:\School\大三\上\软测\code\software-testing`
- 实际执行命令：`mvn "-Dtest=DeepSeekSkillCalculatorTest" test`
- 命令退出码：`1`（BUILD FAILURE，因存在 1 条测试失败；编译与测试发现均成功，非环境错误）
- 测试收集/发现数量：Surefire 报告 `tests="9"`，仅运行目标类 `com.example.lab1.DeepSeekSkillCalculatorTest`（经 `-Dtest` 单类筛选，排除 `CalculatorTest`、`CodexCalculatorRequirementTest`）
- 实际执行数量 / 通过 / 断言失败 / 错误 / 跳过：**9 / 8 / 1 / 0 / 0**
- 执行日志：`docs/lab1/deepseek-skills/maven-test.log`（控制台存档）
- Surefire 报告：
  - `target/surefire-reports/TEST-com.example.lab1.DeepSeekSkillCalculatorTest.xml`
  - `target/surefire-reports/com.example.lab1.DeepSeekSkillCalculatorTest.txt`
  - 存档副本：`docs/lab1/deepseek-skills/surefire-report.xml`、`docs/lab1/deepseek-skills/surefire-report.txt`
- 环境或编译问题：无编译错误；控制台对中文路径显示乱码（Maven 控制台 GBK 编码与读取端 UTF-8 不一致所致），不影响测试结果。实际执行 9 条（> 0），测试有效。

## 5. 覆盖分析
- 统计工具及版本：本轮未启用 JaCoCo（任务未要求行/分支覆盖率）。
- 行/分支覆盖率：未测得（不适用）。
- 条件/判定/语句/路径说明（逻辑推导，非工具实测）：
  - `add` 仅含一个判定 `if (num1 >= 0 && num2 > 0)`，true 分支（返回和）与 false 分支（返回 0）均被用例触发。
  - `num1 >= 0`：true（num1=1/3/1234/0/5）、false（num1=-1）均已覆盖。
  - `num2 > 0`：true（num2=5/1/5678）、false（num2=0/-1/-2）均已覆盖。
  - 短路求值说明：`&&` 左侧 `num1 >= 0` 为 false 时（num1=-1，如 TC07/TC09），右侧 `num2 > 0` 运行时不被求值；此类用例只能证明“左侧 false → 结果 0”，不得虚报为“右侧条件已被求值并判定”。以上为逻辑分析，非覆盖率工具实测，不宣称为条件覆盖/MC-DC/路径覆盖的实测值。

## 6. 失败诊断与缺陷记录
| 记录ID | 对应用例/运行ID | 预期 | 实际 | 失败类别 | 缺陷确认状态 | 证据定位 | 严重程度/说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | TC04 / RUN-20261016-182518 | 0 | 5 | 业务缺陷 | 已确认 | surefire-report.txt L4-L6；Calculator.java L5 | 高（违反 R2 边界规则） |

- 失败分类结论：唯一失败为“已确认业务缺陷”，非规格不清、测试代码错误或环境异常（论证见 `defects.md`）。
- 独立缺陷数量：**1**。

## 7. 复现步骤和证据
- 最短复现命令：`mvn "-Dtest=DeepSeekSkillCalculatorTest" test`（或直接 `new Calculator().add(0, 5)`）
- 失败用例定位：`DeepSeekSkillCalculatorTest.firstZeroSecondPositiveReturnsZero`（测试源码第 50 行），断言 `assertEquals(0, calculator.add(0, 5))`
- 日志/报告：`maven-test.log`、`surefire-report.txt`（第 4–6 行）、`surefire-report.xml`（`<failure message="expected: <0> but was: <5>">`）
- 建议人工截图：测试源码 + 断言、VS Code Testing 面板、终端 `mvn` 输出。

## 8. 总结与限制
- 本轮证据支持的结论：`Calculator.add` **不满足**功能需求 R2。当第一个参数为 0、第二个参数为正数时，实际返回第二个参数的值（如 `add(0,5)=5`），而非 0。根因是 `Calculator.java` 第 5 行判定使用 `num1 >= 0`，应为 `num1 > 0`。
- 未验证范围：int 整数溢出场景（如 `Integer.MAX_VALUE + 1`）不在需求明确范围内，本轮未纳入用例，也未据此判定缺陷。
- 下一步建议：不自动修改原程序；建议在用户授权后将 `num1 >= 0` 改为 `num1 > 0` 并复测。
- 变更文件清单：
  - 新增：`src/test/java/com/example/lab1/DeepSeekSkillCalculatorTest.java`
  - 新增：`docs/lab1/deepseek-skills/` 下全部产物
  - 未修改：`Calculator.java`、`pom.xml`、已有测试文件、`software-testing-lab` 任何文件。

## 附录：源码快照（发放版本，未修改）
```java
package com.example.lab1;

public class Calculator {
    public int add(int num1, int num2) {
        if (num1 >= 0 && num2 > 0) {
            return num1 + num2;
        } else {
            return 0;
        }
    }
}
```
