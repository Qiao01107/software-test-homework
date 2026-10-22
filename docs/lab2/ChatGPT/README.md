# Lab2 ChatGPT 测试材料

本证据包针对用户提供的实验二 `Example(int x,int y,int z)` 方法。原始截图仅包含方法体，`src/main/java/com/example/lab2/Calculator.java` 额外添加了 `package` 和 `Calculator` 类外壳，以便独立编译，**方法内的原始业务逻辑未修改**。

## 文件说明

- `report.md`：实验报告第四部分，可复制到 Word。
- `test_cases.csv`：7 条用例的输入、预期值、Java 实测输出、条件取值与覆盖目的。
- `coverage_analysis.md`：四类覆盖的逻辑证明以及 `&&`、`||` 短路处理。
- `verification.log`：**真正执行过的普通 Java 21** 编译与测试日志（不是 JUnit 日志）。
- `src/main/java/com/example/lab2/Calculator.java`：按截图还原的被测方法，增加包名与类外壳。
- `src/test/java/com/example/lab2/ChatGPTLab2CoverageTest.java`：可复制到课程项目的 **JUnit 5** 源码（本环境未执行）。
- `src/verification/ChatGPTLab2JavaVerifier.java`：本环境真实运行的 Java 验证程序。

## 在 Windows / VS Code / Maven 中执行 JUnit 5

1. 确认项目中 `src/main/java/com/example/lab2/Calculator.java` 有 `com.example.lab2.Calculator` 类，且存在方法名大小写一致的 `Example(int,int,int)`。
2. 仅将 `src/test/java/com/example/lab2/ChatGPTLab2CoverageTest.java` 复制到你现有课程 Maven 项目的对应测试目录。不要覆盖或修改已有业务源码。
3. 在 `D:\School\3\up\软测\code\software-testing` 项目根目录执行：
   `mvn "-Dtest=ChatGPTLab2CoverageTest" test`
4. 核实 Maven 日志中目标测试类实际被执行，记录 `Tests run` 和 Surefire 报告，并截图：测试代码 + 测试用例状态 + Maven 执行结果。
5. 即使全部 JUnit 断言通过，也只能说明选定输入的结果正确，四种覆盖要求还需结合 `coverage_analysis.md` 的求值矩阵核实。

## 独立验证命令（非 JUnit）

Linux 中使用 JDK 21 执行（日志已保存）：

```bash
javac -encoding UTF-8 -d build src/main/java/com/example/lab2/Calculator.java src/verification/ChatGPTLab2JavaVerifier.java
java -cp build com.example.lab2.ChatGPTLab2JavaVerifier
```

**禁止混淆执行口径：已执行 Java 7/7；JUnit 5 在当前容器未执行，不能声称其已通过。**
