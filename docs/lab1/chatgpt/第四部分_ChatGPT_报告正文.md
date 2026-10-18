# 四、ChatGPT 辅助单元测试

## 4.1 测试目的与实验范围

在人工 JUnit 测试之外，本实验使用 ChatGPT 对题目提供的 Calculator.add(int,int) 进行一轮补充验证，考察其依据需求设计测试用例、通过实际运行检查输出、分析异常结果的能力。功能规则为：仅当 num1>0 且 num2>0 时返回两数之和；任何一个输入小于或等于 0 则返回 0。

本次直接使用题目所给原始 Java 代码，保留其 num1>=0 的实现，不修改业务逻辑。题目已明确给出故意设置的缺陷，所以本次结果属于对已提示问题的测试复现和定位验证，而不是在未知答案条件下独立发现隐藏缺陷。

## 4.2 测试设计

ChatGPT 根据功能需求采用等价类划分和边界值分析，分别考虑两个参数均为正整数、任一参数为 0、任一参数为负整数及其组合，共选取 12 条测试数据。期望输出全部从功能需求推导，未把被测程序输出当作正确答案。


**测试用例及实测结果**

| 编号 | 输入 | 期望 | 实际 | 结果 |
|---|---|---:|---:|---|
| TC01 | (1,2) | 3 | 3 | PASS |
| TC02 | (4,5) | 9 | 9 | PASS |
| TC03 | (0,1) | 0 | 1 | FAIL |
| TC04 | (0,7) | 0 | 7 | FAIL |
| TC05 | (1,0) | 0 | 0 | PASS |
| TC06 | (0,0) | 0 | 0 | PASS |
| TC07 | (-1,2) | 0 | 0 | PASS |
| TC08 | (2,-1) | 0 | 0 | PASS |
| TC09 | (-1,-1) | 0 | 0 | PASS |
| TC10 | (-1,0) | 0 | 0 | PASS |
| TC11 | (0,-1) | 0 | 0 | PASS |
| TC12 | (10,20) | 30 | 30 | PASS |

## 4.3 测试执行与实际结果

当前测试环境为 Linux 上的 OpenJDK 21.0.12.1，使用 javac 编译原始 Calculator.java 和独立 Java 直接调用验证程序，然后使用 java 执行并保存控制台原始日志。编译成功；12 组数据均实际调用 Calculator.add()，10 组输出与期望一致，2 组不一致。验证程序检测到不一致后以退出码 1 结束。失败用例分别为 add(0,1)（期望 0，实际 1）和 add(0,7)（期望 0，实际 7）。两条失败涉及相同的判断条件问题，因此只计 1 个独立业务缺陷。

## 4.4 缺陷原因分析

原代码条件为 if (num1 >= 0 && num2 > 0)。当 num1=0、num2>0 时该条件成立，进入求和分支，错误返回正整数；按题目要求应返回 0。正确的需求条件为 if (num1 > 0 && num2 > 0)。本次没有修改被测源文件或更改预期结果。

## 4.5 JUnit 5 测试代码与执行状态

为了对接课程的 JUnit 实验，本次另外编写了标准 JUnit 5 测试类 ChatGPTCalculatorTest.java，包含与上述 12 组输入对应的 12 个 @Test 方法，使用 assertEquals(expected, actual) 定义断言。提供了符合题目 package study.myconnect.cn 的独立项目版本及适配现有 Maven 项目 package com.example.lab1 的版本。

需要如实说明：当前执行环境没有 Maven 和 JUnit 5 依赖，且无法通过网络获取，因此这 12 条 JUnit 测试尚未在本次环境中真实执行；上述“10 通过、2 失败”属于实际执行的普通 Java 直接调用验证，不能写成 JUnit/Surefire 的实际统计。若需要在报告中放置 JUnit 通过/失败截图，应在已配置 Maven 与 JUnit 5 的 VS Code 项目中单独执行 mvn "-Dtest=ChatGPTCalculatorTest" test，并保存真实的 Surefire 日志和截图。

## 4.6 测试小结

本轮 ChatGPT 补充验证设计并实际执行了 12 组输入，验证了正常加法、零边界与负数输入的程序行为，复现并定位了 1 个边界判断缺陷。结果说明边界值测试有助于发现正常输入无法暴露的错误，也说明 AI 可以辅助完成用例设计与结果分析。但本轮未实际运行 JUnit 引擎，正式 JUnit 执行结论应以补跑后的 Maven/Surefire 证据为准。

**实际运行命令**

```bash
javac -encoding UTF-8 -d build src/main/java/study/myconnect/cn/Calculator.java verification/CalculatorIndependentCheck.java
java -cp build study.myconnect.cn.CalculatorIndependentCheck
```

**原始执行证据**：`evidence/direct-java-check.log`（另有运行日志排版图，仅为展示用途，非 IDE 截屏）。
