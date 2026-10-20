# Lab2 白盒测试用例清单

## 1. 条件与判定记号

以 `Calculator.Example(int x, int y, int z)` 的实际源码为准：

- A：`x >= 3`
- B：`y == 0`
- D1：`A && B`
- C：`z <= 5`
- D：`x < z`
- D2：`C || D`

表中 `T`、`F` 分别表示该条件被实际求值且结果为真、假；`NE` 表示因 Java 短路规则未被求值（not evaluated），不能作为条件覆盖证据。

## 2. 测试用例

| 编号 | 输入 `(x,y,z)` | A | B | D1 | C | D | D2 | 预期输出推导 | 预期 | 实际 | 结果 | 主要覆盖目的 |
|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|---|---:|---:|:---:|---|
| TC01 | `(3,0,5)` | T | T | T | T | NE | T | `result=0`；D1 真，`result=5+3=8`；C 真使 `||` 短路，`result=8+3=11` | 11 | 11 | 通过 | D1 真；A、B、C 为真；执行第一个 `if` 体和第二个 `if` 真分支 |
| TC02 | `(2,1,6)` | F | NE | F | F | T | T | `result=0`；A 假使 `&&` 短路；C 假后 D 真，`result=0+2=2` | 2 | 2 | 通过 | A 假；C 假且 D 真；证明 D2 可由右条件取真 |
| TC03 | `(6,1,6)` | T | F | F | F | F | F | `result=0`；D1 假，不改值；D2 假，执行 `else`，`result=0+1=1` | 1 | 1 | 通过 | B 假；D2 假；执行 `else`；补齐两判定的假结果 |

短路条件的理论值与实际求值必须区分：

- TC01 中表达式 `x < z` 从参数看为真，但 C 已为真，D 实际未求值，因此记为 `NE`。
- TC02 中表达式 `y == 0` 从参数看为假，但 A 已为假，B 实际未求值，因此记为 `NE`。
- TC03 中四个基本条件均实际求值，其中 A 为真、B/C/D 为假。

## 3. 各覆盖标准采用的用例集合

| 覆盖标准 | 用例集合 | 逻辑证据 | 是否满足 |
|---|---|---|:---:|
| 语句覆盖 | TC01、TC03 | TC01 执行 `result=z+x` 与 `result=result+x`；TC03 执行 `result=result+y`；初始化和 `return` 均执行 | 是 |
| 判定覆盖 | TC01、TC03 | D1：TC01=T、TC03=F；D2：TC01=T、TC03=F | 是 |
| 条件覆盖 | TC01、TC02、TC03 | A：T/F；B：T/F（均实际求值）；C：T/F；D：TC02=T、TC03=F（均实际求值） | 是 |
| 条件/判定覆盖 | TC01、TC02、TC03 | 同时具备上述全部基本条件 T/F 和 D1、D2 的 T/F | 是 |

## 4. JUnit 5 映射

| 用例 | 测试方法 |
|---|---|
| TC01 | `bothDecisionsTrueWithAndRightConditionEvaluatedAndOrShortCircuited` |
| TC02 | `firstDecisionFalseByLeftConditionAndSecondDecisionTrueByRightCondition` |
| TC03 | `bothDecisionsFalseAndElseBranchExecuted` |

本测试类包含 3 个普通 `@Test` 方法，没有参数化测试；因此测试方法数和实际调用次数均为 3。

## 5. 失败用例

无。三条用例的实际输出均与独立推导的预期输出一致，Surefire 报告中失败数和错误数均为 0。
