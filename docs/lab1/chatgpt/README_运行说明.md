# 实验一：ChatGPT 测试证据与 JUnit 5 复现说明

## 已完成（在当前环境真实执行）
- Java 21（OpenJDK 21.0.12.1）编译了题目原始 `Calculator.java` 和独立直接调用测试程序。
- 实际执行 12 组输入：10 通过，2 失败；失败分别为 `(0,1)` 和 `(0,7)`。
- 原始记录：`evidence/direct-java-check.log`。
- 注意：此运行是**普通 Java 直接调用核验，不是 JUnit 5**；不能把该结果写作 Surefire/JUnit 统计。
- 题目已经指出原始缺陷，因此本次属于复现与验证已提示的缺陷，不应称未知缺陷盲测发现。

## 如何在你现有的 Windows Maven 项目中执行真正的 JUnit 5
现有项目若使用 `package com.example.lab1`，无需修改 Calculator.java：

1. 将 `for-existing-project/ChatGPTCalculatorTest.java` 复制到
   `D:\School\大三\上\软测\code\software-testing\src\test\java\com\example\lab1\ChatGPTCalculatorTest.java`
2. 打开 VS Code 终端并切换到**包含 pom.xml 的项目根目录**：
   ```powershell
   cd "D:\School\大三\上\软测\code\software-testing"
   mvn "-Dtest=ChatGPTCalculatorTest" test
   ```
3. 在控制台确认 `Running com.example.lab1.ChatGPTCalculatorTest` 及真正的 `Tests run` 行；原代码预期会出现两条断言失败。退出码非零属正常的缺陷检测结果。
4. 截图时将 JUnit 测试源码、VS Code 测试面板、终端执行统计一起保留。
5. 留存 `target/surefire-reports/TEST-com.example.lab1.ChatGPTCalculatorTest.xml` 与 `.txt`。如果不存在，请先检查 Maven 是否真正执行到测试阶段。

本文件里的 `src/test/java/study/myconnect/cn/ChatGPTCalculatorTest.java` 与题目最初给出的 `package study.myconnect.cn` 匹配；可在独立 Maven 项目内运行，命令相同但包名不同。

## 复现普通 Java 验证（无需 Maven/JUnit）
```bash
mkdir -p build
javac -encoding UTF-8 -d build src/main/java/study/myconnect/cn/Calculator.java verification/CalculatorIndependentCheck.java
java -cp build study.myconnect.cn.CalculatorIndependentCheck
```
程序退出码为 1 表示检测到与需求不符的输出，并非编译环境报错。
