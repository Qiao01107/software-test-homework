# 缺陷记录 —— DeepSeek V4 Pro + Skills 组（实验一）

## 缺陷 D1

| 项 | 内容 |
| --- | --- |
| 记录ID | D1 |
| 对应用例 | TC04（`firstZeroSecondPositiveReturnsZero`） |
| 运行ID | RUN-20261016-182518 |
| 输入 | num1 = 0, num2 = 5 |
| 预期输出 | 0（需求 R2：任一整数 <= 0 即返回 0，0 满足 <= 0） |
| 实际输出 | 5 |
| 失败类别 | 业务缺陷（已确认） |
| 涉及需求 | R2 |

### 现象
`Calculator.add(0, 5)` 返回 5，而按需求应返回 0。

### 根因分析
`src/main/java/com/example/lab1/Calculator.java` 第 5 行：

```java
if (num1 >= 0 && num2 > 0) {
```

判定对第一个参数使用了 `num1 >= 0`，与需求“两个整数都**大于 0**”不符，应为 `num1 > 0`。
当 `num1 = 0` 且 `num2 > 0` 时：`num1 >= 0` 为 true、`num2 > 0` 为 true，错误进入求和分支，返回 `0 + num2 = num2`。

### 缺陷确认过程（排除测试与环境原因）
1. 编译/构建正常：`compiler:3.13.0:testCompile` 成功，Surefire 自动检测 JUnitPlatformProvider。
2. 目标测试被发现并执行：Surefire 报告 `tests="9"`，实际执行 9 条（> 0）。
3. 测试断言正确：`assertEquals(0, calculator.add(0, 5))` 严格编码需求 R2（0 <= 0 → 返回 0），未采用程序实际输出作为预期。
4. 行为可复现：Surefire 失败堆栈 `expected: <0> but was: <5>` 与源码逻辑（`num1 >= 0` 对 0 为 true）一致。
→ 结论：**已确认业务缺陷**（1 个独立缺陷）。

### 严重程度
高：违反边界规则，`add(0, 正数)` 这一类输入全部返回错误结果。

### 复现步骤
1. 进入 `D:\School\大三\上\软测\code\software-testing`
2. 执行：`mvn "-Dtest=DeepSeekSkillCalculatorTest" test`
3. 观察 Surefire 报告：`DeepSeekSkillCalculatorTest.firstZeroSecondPositiveReturnsZero ... expected: <0> but was: <5>`
   或直接调用 `new Calculator().add(0, 5)` 得到 5。

### 证据定位
- `docs/lab1/deepseek-skills/maven-test.log`
- `docs/lab1/deepseek-skills/surefire-report.txt`（第 4–6 行）
- `docs/lab1/deepseek-skills/surefire-report.xml`（`<failure message="expected: <0> but was: <5>">`）

### 建议修复（不自动修改）
将 `Calculator.java` 第 5 行 `num1 >= 0` 改为 `num1 > 0`。
