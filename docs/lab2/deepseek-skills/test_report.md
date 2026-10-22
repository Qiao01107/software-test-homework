# 实验二 JUnit 5 白盒测试报告（DeepSeek V4 Pro + Skills 组）

> 测试组：DeepSeek V4 Pro + software-testing-lab Skill 独立实验组
> 被测方法：`com.example.lab2.Calculator#Example(int x, int y, int z)`
> 覆盖标准：语句覆盖 / 判定覆盖 / 条件覆盖 / 条件-判定覆盖

## 1. 实验基本信息

- **实验编号/名称**：实验二 —— 白盒测试（四种覆盖标准）
- **测试组及方式**：DeepSeek V4 Pro + `software-testing-lab` Skill，独立实验组；`task_mode = execute`
- **测试目标与版本**：`Calculator.java`（lab2 包），源码未修改
- **实验目的**：独立设计并实际执行满足语句覆盖、判定覆盖、条件覆盖、条件/判定覆盖的 JUnit 5 测试，验证 Skill 能否指导 AI 完成用例设计与真实执行。
- **约束和独立性说明**：
  - 只读业务源码，未修改 `Calculator.java`、`pom.xml`。
  - 未读取 `docs/lab2/codex/` 等其他组的测试代码、报告与历史结果；未阅读项目中已有其他测试类内容（`CalculatorTest.java`、`CodexLab2CoverageTest.java` 等）。
  - 仅新增本组测试类与 `docs/lab2/deepseek-skills/` 交付物。

## 2. 环境与范围

- **OS**：Windows 11（`os.name=Windows 11`，`os.version=10.0`，amd64）
- **Java**：Oracle JDK 21.0.11（`21.0.11+9-LTS-211`，位于 `D:\CodeTools\Java\jdk-21.0.11`）
- **Maven**：Apache Maven 3.9.16（位于 `D:\CodeTools\Apache\apache-maven-3.9.16`）
- **测试框架及依赖**：JUnit Jupiter 5.12.2；`maven-surefire-plugin` 3.5.2；`maven-compiler-plugin` 3.13.0（`release=21`）
- **JVM 编码**：`file.encoding=UTF-8`，`stdout.encoding=GBK`，`native.encoding=GBK`
- **被测路径**：`src/main/java/com/example/lab2/Calculator.java`（方法 `Example(int,int,int)`）
- **源码版本标识（无 git commit，用 SHA256）**：
  - `Calculator.java`：`9B4D4938FBAF69AB698D7E6F4342D1DF58EB00C1AAB0CF826ABEE65A93908E20`
  - `pom.xml`：`7AAFA0A106558451D80BC7E13FE39C66ADA23625E8918572507F823FDBB50BAA`
  - 本组测试类 `DeepSeekSkillLab2CoverageTest.java`：`8B014B4370084BEB08DC802922BAFA302BC224D77C1468A30F0A050A8E7D778C`
- **环境准备/变更记录**：未修改业务代码与构建配置。执行期遇到 DeepSeek Harness Windows 沙箱 ACL 错误（`SetNamedSecurityInfoW failed (Win32 5): grantWrite(...)`），按用户要求通过界面申请**仅针对 Maven 命令的单次受控授权**后执行，未修改 Windows ACL、未授予持续权限（详见 §4）。

## 3. 需求分析与测试设计

### 3.1 业务规则与规格说明

被测方法 `Example` 为实验二的待测函数，**未提供独立功能规格文档**。依据 Skill 纪律「绝不能将程序实际行为直接当作正确结果」，本组期望输出由**人工按代码语义逐句推导**得到（见 `test_cases.md` §4），并以此作为断言 oracle；未直接采用程序运行输出充当正确答案。本方法无外部依赖、无 I/O，纯确定性计算，适合白盒覆盖测试。

### 3.2 控制流与覆盖要素

```java
public int Example(int x, int y, int z){
    int result = 0;                          // S1
    if(x >= 3 && y == 0){                    // D1 = C1 && C2
        result = z + x;                      // S2
    }
    if(z <= 5 || x < z){                     // D2 = C3 || C4
        result = result + x;                 // S3
    } else {
        result = result + y;                 // S4
    }
    return result;                           // S5
}
```

| 类别 | 要素 |
| --- | --- |
| 可执行语句（5） | S1 `result=0`；S2 `result=z+x`；S3 `result=result+x`；S4 `result=result+y`；S5 `return result` |
| 复合判定（2） | D1 = `x>=3 && y==0`；D2 = `z<=5 || x<z` |
| 基本条件（4） | C1 `x>=3`；C2 `y==0`；C3 `z<=5`；C4 `x<z` |
| 分支（4） | D1 真/假（假为隐式无 else 落入下一条 if）、D2 真/假（else） |

### 3.3 短路求值处理

- `&&`：C1=F 时 C2 不求值（NE）；`||`：C3=T 时 C4 不求值（NE）。
- 因此 C2 仅在 C1=T 时可被求值，C4 仅在 C3=F 时可被求值。
- NE 不产生真/假取值，**不计入条件覆盖**。

### 3.4 用例清单

| 用例ID | 输入 (x,y,z) | 期望输出 | C1 | C2 | D1 | C3 | C4 | D2 | 覆盖目的 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC01 | (3,0,5) | 11 | T | T | T | T | NE | T | S2、S3；`||` 短路；D1 真、D2 真 |
| TC02 | (2,1,7) | 2 | F | NE | F | F | T | T | `&&` 短路；C4=T；S3 |
| TC03 | (5,1,3) | 5 | T | F | F | T | NE | T | C2=F 使 D1 假；补充组合 |
| TC04 | (8,2,6) | 2 | T | F | F | F | F | F | C4=F；D2 假走 else 执行 S4 |

需求/覆盖追踪与完整矩阵见 `test_cases.md`。

## 4. 执行结果

- **执行状态**：已执行（真实运行，非仅生成代码）。
- **工作目录**：`D:\School\3\up\软测\code\software-testing`
- **实际执行命令**：`mvn "-Dtest=DeepSeekSkillLab2CoverageTest" test`

### 运行记录

| 运行ID | 时间（+08:00） | 退出码 | 关键输出 | 测试统计 |
| --- | --- | --- | --- | --- |
| RUN1 | 2026-10-20 19:03:45 | 0 | 首次编译 6 个测试源文件（含新增本组类），BUILD SUCCESS | 4 run / 0 fail / 0 error / 0 skip（0.045 s） |
| RUN2 | 2026-10-20 21:54:17 | 0 | 复跑复现，BUILD SUCCESS（总耗时 1.452 s） | 4 run / 0 fail / 0 error / 0 skip（0.036 s） |

- **测试收集/发现数**：目标类 `com.example.lab2.DeepSeekSkillLab2CoverageTest` 被 Surefire 发现并执行，**实际执行 4 条**（>0，满足要求）。
- **实际执行数量 / 通过 / 断言失败 / 错误 / 跳过**：**4 / 4 / 0 / 0 / 0**。
- **执行日志路径**：`docs/lab2/deepseek-skills/maven-test.log`（RUN2 原文，UTF-8 规范化）。
- **测试报告路径**：`docs/lab2/deepseek-skills/surefire-report.txt`、`surefire-report.xml`（原样复制自 `target/surefire-reports`）。
- **环境或编译问题及修复记录**：DeepSeek Harness 沙箱默认 `workspace-write` 模式对工作目录授予写权限失败（`SetNamedSecurityInfoW failed (Win32 5)`），普通 pwsh/Maven 命令被拒。按用户指示，仅针对必要 Maven 命令通过界面申请单次受控授权后正常执行；**未**自行修改 Windows ACL、未运行权限修复脚本、未授予持续全局权限。此问题属环境授权边界，与测试结果无关，测试本身 0 失败。

## 5. 覆盖分析

- **覆盖率工具**：未使用 JaCoCo 等工具（`pom.xml` 未配置）。**因此本报告不提供、也不虚构工具实测的行/分支覆盖率百分比。**
- **覆盖口径**：四种覆盖标准通过「用例—真值矩阵」进行逻辑证明，口径如下。

### 5.1 语句覆盖（满足，TC01+TC04 即可，全套件 4 条均满足）

S1、S5 被所有用例执行；S2 由 TC01（D1=T）执行；S3 由 TC01（D2=T）执行；S4 由 TC04（D2=F）执行。5 条可执行语句全部至少执行一次。

### 5.2 判定覆盖（满足，TC01+TC04 即可）

D1=T（TC01）、D1=F（TC04）；D2=T（TC01）、D2=F（TC04）。两个复合判定均取到真、假。

### 5.3 条件覆盖（满足，TC01+TC02+TC04）

- C1：T（TC01）/ F（TC02）
- C2：T（TC01）/ F（TC04）（TC02 中为 NE，不计入）
- C3：T（TC01）/ F（TC02）
- C4：T（TC02）/ F（TC04）（TC01、TC03 中为 NE，不计入）

四个基本条件均取到真、假。

### 5.4 条件/判定覆盖（满足，TC01+TC02+TC04）

上述条件覆盖与判定覆盖同时成立，故条件/判定覆盖满足。

### 5.5 短路求值与不可达说明

- C2 在 TC02 中因 `&&` 短路为 NE；C4 在 TC01、TC03 中因 `||` 短路为 NE。
- 这些 NE 未计入条件覆盖（未执行的条件不虚报）。
- 无不可达语句；两个 if 的假分支均可达（D1 假为隐式落入，D2 假为 else）。

## 6. 失败诊断与缺陷记录

| 记录ID | 对应用例/运行ID | 预期 | 实际 | 失败类别 | 缺陷确认状态 | 证据定位 | 严重程度/说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — | — | 无失败、无运行错误 |

- **结论**：4 条用例全部通过，**无断言失败、无运行错误、无跳过**。
- **业务问题**：本实验范围内**未发现业务缺陷**。`Example` 逻辑简单确定，无规格冲突、无崩溃、无异常路径。已确认缺陷数 = 0。
- **未验证范围/限制**：未做整型溢出（如极大 `x + z`）、负极大值、`int` 边界等健壮性测试；本实验聚焦四种覆盖标准，未覆盖此类非功能性边界。

## 7. 复现步骤和证据

- **最短复现命令**：
  ```bash
  cd D:\School\3\up\软测\code\software-testing
  mvn "-Dtest=DeepSeekSkillLab2CoverageTest" test
  ```
- **日志/报告文件**：
  - `maven-test.log`（RUN2 原始日志）
  - `surefire-report.txt`（摘要：4 run / 0 / 0 / 0）
  - `surefire-report.xml`（`<testsuite tests="4" failures="0" errors="0" skipped="0">`，4 个 `<testcase>` 即 TC01~TC04）
- **失败用例定位**：无（0 失败）。
- **建议人工截图内容**：`DeepSeekSkillLab2CoverageTest.java` 源码与断言、VS Code Testing 面板 4/4 通过、终端 `mvn` 输出。

## 8. 总结与限制

### 8.1 Skill 作用评估

`software-testing-lab` Skill 在本次实验中**实际读取并全程使用**（直接文件读取方式，证据见 `skill-loading-evidence.md`）。它提供的是**可复现的工作流程与纪律**，而非用例库或自动通过保证：

- **成功指导**：确认 `execute` 模式并强制真实运行；界定独立性/变更边界（只读业务源码、不读其他组产物）；明确白盒四种覆盖；要求区分短路求值的 T/F/NE 且 NE 不计入条件覆盖；要求区分「测试失败」与「环境失败」；禁止虚构覆盖率；提供 8 节报告模板组织报告。
- **局限**：
  1. Skill 是流程文档，**不生成测试用例**——本组用例由人工控制流分析推导；
  2. 不含 JUnit 5 API 细节或 Maven 命令语法，需依赖既有知识；
  3. 未预判 Windows 沙箱 ACL 授权问题（按用户指示走界面单次授权解决，非 Skill 条款）；
  4. 无法提供覆盖率工具实测值——Skill 反而要求不得把逻辑证明混同于工具实测百分比，本组如实遵守。

### 8.2 本轮证据支持的结论

- 设计了 4 条 JUnit 5 用例，**实际执行 4 条、4 通过、0 失败、0 错误、0 跳过**（RUN1/RUN2 两次一致）。
- 四种覆盖标准均满足，覆盖满足性由真值矩阵逻辑证明，未虚构工具实测覆盖率。
- Java `&&`、`||` 短路求值已正确处理（T/F/NE 区分），NE 未计入条件覆盖。
- 未发现业务缺陷，未修改业务代码。

### 8.3 变更文件清单

- 新增：`src/test/java/com/example/lab2/DeepSeekSkillLab2CoverageTest.java`
- 新增：`docs/lab2/deepseek-skills/` 下 7 个交付文件（`test_report.md`、`test_cases.md`、`maven-test.log`、`surefire-report.txt`、`surefire-report.xml`、`skill-loading-evidence.md`、`README.md`）
- 修改：无（`Calculator.java`、`pom.xml` 均未改动）
