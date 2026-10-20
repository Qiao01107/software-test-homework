# Lab2 JUnit 5 白盒测试报告（Codex 普通模式独立测试）

## 1. 测试范围与约束

- 项目根目录：`D:\School\3\up\软测\code\software-testing`
- 被测类：`src/main/java/com/example/lab2/Calculator.java`
- 被测方法：`Calculator.Example(int x, int y, int z)`
- 测试类：`src/test/java/com/example/lab2/CodexLab2CoverageTest.java`
- 执行日期：2026-10-19（Asia/Shanghai）
- 本次未使用 Agent Skill、其他组测试代码、既有 Lab2 测试代码或历史结论。
- 未修改 `Calculator.java`、`pom.xml` 或其他项目配置。
- 未使用 JaCoCo 等覆盖率工具；本报告只依据源码控制流、短路求值和已执行用例给出逻辑覆盖结论，不声明工具实测覆盖率百分比。

## 2. 实际读取的文件

测试设计前读取：

1. `src/main/java/com/example/lab2/Calculator.java`
2. `pom.xml`

执行后为核验结果读取：

3. `target/surefire-reports/com.example.lab2.CodexLab2CoverageTest.txt`
4. `target/surefire-reports/TEST-com.example.lab2.CodexLab2CoverageTest.xml`
5. `docs/lab2/codex/maven-test.log`

只枚举了项目文件名以确认路径；未打开或参考原有 `src/test/java/com/example/lab2/CalculatorTest.java` 以及人工组、ChatGPT 组、Skills 组或其他 AI 组的测试/报告内容。

## 3. 项目配置与执行环境

`pom.xml` 的相关配置如下：

- Java 编译目标：release 21
- JUnit Jupiter：5.12.2（test scope）
- Maven Compiler Plugin：3.13.0
- Maven Surefire Plugin：3.5.2

实际环境由 `mvn -version` 和 Surefire XML 核验：

- Apache Maven：3.9.16
- Java：Oracle JDK 21.0.11
- 操作系统：Windows 11 amd64
- 时区：Asia/Shanghai
- Surefire 实际提供者：`org.apache.maven.surefire.junitplatform.JUnitPlatformProvider`

## 4. 源码控制流分析

### 4.1 基本条件与复合判定

- A：`x >= 3`
- B：`y == 0`
- D1：`A && B`
- C：`z <= 5`
- D：`x < z`
- D2：`C || D`

Java 短路规则：D1 中 A 为假时 B 不求值；D2 中 C 为真时 D 不求值。因此条件覆盖必须由“实际求值”的 T/F 证明，不能用未执行条件的理论真假代替。

### 4.2 可执行语句与分支

识别出的主要可执行语句：

- S1：`int result = 0`
- S2：`result = z + x`（D1 真分支）
- S3：`result = result + x`（D2 真分支）
- S4：`result = result + y`（D2 假分支/`else`）
- S5：`return result`

判定分支：D1 的真/假结果；D2 的真/假结果。D1 没有显式 `else`，其假结果表现为跳过 S2。

## 5. 用例预期值的独立推导

### TC01：`(3,0,5)`，预期 11

1. `result=0`。
2. A、B 均真，D1 真，执行 S2：`result=5+3=8`。
3. C 真，D 因 `||` 短路未求值，D2 真，执行 S3：`result=8+3=11`。
4. 返回 11。

### TC02：`(2,1,6)`，预期 2

1. `result=0`。
2. A 假，B 因 `&&` 短路未求值，D1 假，跳过 S2。
3. C 假，继续求值 D；`2<6` 为真，D2 真，执行 S3：`result=0+2=2`。
4. 返回 2。

### TC03：`(6,1,6)`，预期 1

1. `result=0`。
2. A 真、B 假，D1 假，跳过 S2。
3. C 假、D 也假，D2 假，执行 S4：`result=0+1=1`。
4. 返回 1。

预期输出在运行被测程序前按上述语句顺序推导，没有把程序当前输出反向当作预期值。

## 6. 四种覆盖标准分析

### 6.1 语句覆盖

覆盖要求：每条可执行语句至少执行一次。

采用 TC01、TC03。TC01 覆盖 S1、S2、S3、S5；TC03 覆盖 S1、S4、S5。S1 至 S5 均有执行证据，因此语句覆盖要求满足。

### 6.2 判定覆盖

覆盖要求：每个复合判定的真、假结果均至少出现一次。

采用 TC01、TC03：

- D1：TC01 为真；TC03 为假。
- D2：TC01 为真；TC03 为假。

两个判定的两种结果均覆盖，因此判定覆盖要求满足。

### 6.3 条件覆盖

覆盖要求：每个基本条件在实际被求值时，真、假结果均至少出现一次。

采用 TC01、TC02、TC03：

- A：TC01/TC03 为真，TC02 为假。
- B：TC01 为真，TC03 为假；二者都在 A 为真后实际求值。
- C：TC01 为真，TC02/TC03 为假。
- D：TC02 为真，TC03 为假；二者都在 C 为假后实际求值。

TC01 中 D 未求值、TC02 中 B 未求值，均未误计为覆盖。四个基本条件均取得实际求值的真、假结果，因此条件覆盖要求满足。

### 6.4 条件/判定覆盖

覆盖要求：同时满足条件覆盖与判定覆盖。

采用 TC01、TC02、TC03。该集合既使 A、B、C、D 各自实际取得 T/F，又使 D1、D2 各自取得 T/F，因此条件/判定覆盖要求满足。

详细条件矩阵见 `test_cases.md`。

## 7. JUnit 5 实现与执行

测试类使用 3 个普通 `@Test` 方法，每个方法对应一个用例；未使用参数化测试。因此：

- 测试方法数量：3
- 实际测试调用次数：3

最终执行命令（工作目录均为项目根目录）：

```powershell
mvn --no-transfer-progress "-Dstyle.color=never" "-Dtest=CodexLab2CoverageTest" test
```

退出码：0。`-Dtest=CodexLab2CoverageTest` 将 Surefire 执行范围限定为本次 Codex 测试类。Surefire XML 的 `test` 属性也记录为 `CodexLab2CoverageTest`，证明不是把其他测试类计入总数。

## 8. 实际执行结果

| 指标 | 数量 |
|---|---:|
| 测试方法 | 3 |
| 实际测试调用 | 3 |
| 通过 | 3 |
| 失败 | 0 |
| 错误 | 0 |
| 跳过 | 0 |

实际输出：

- TC01：11（期望 11，通过）
- TC02：2（期望 2，通过）
- TC03：1（期望 1，通过）

Maven 最终状态为 `BUILD SUCCESS`，完成时间为 `2026-10-19T21:37:44+08:00`。原始控制台日志见 `maven-test.log`；Surefire 原始 XML 和文本摘要分别见 `surefire-report.xml`、`surefire-report.txt`。

控制台开头保留了一行启动器级别的 `Access is denied.`，同时日志后续显示 Maven 正常扫描、编译、执行 3 个测试并以退出码 0 完成。该信息没有造成测试发现、测试执行或报告生成失败；未删除或伪造该行。

## 9. 失败与问题记录

- 失败用例：无，故不存在需记录的失败输入、期望/实际差异或断言信息。
- 被测程序问题：本次三个覆盖用例均符合独立推导的预期，未发现可由这些用例证明的业务逻辑缺陷。
- 环境提示：存在上述 `Access is denied.` 启动提示，但 Maven/Surefire 的退出码、构建结果和报告均正常；它属于环境/启动器提示，不是被测业务程序失败。

## 10. 结论与限制

四种要求均由逻辑分析及实际执行证据满足：语句覆盖、判定覆盖使用 TC01+TC03；条件覆盖、条件/判定覆盖使用 TC01+TC02+TC03。全部 3 次测试调用通过，没有修改被测业务逻辑。

本次没有使用覆盖率插桩工具，所以结论是针对已识别控制流的逻辑覆盖结论，而非 JaCoCo 等工具给出的数值覆盖率。除该数值覆盖率未采集外，请求中的源码分析、用例设计、JUnit 5 实现、限定类执行、原始日志保存、Surefire 核验和中文报告均已完成。
