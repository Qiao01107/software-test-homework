# 测试用例清单 —— DeepSeek V4 Pro + Skills 组（实验一）

- 被测类：`com.example.lab1.Calculator#add(int num1, int num2)`
- 测试类：`com.example.lab1.DeepSeekSkillCalculatorTest`
- 测试方法：黑盒等价类划分 + 边界值分析
- 期望值来源：用户功能需求（非程序当前输出）

| 用例ID | 测试方法 | 输入 (num1, num2) | 期望输出 | 实际输出 | 结果 | 测试技术 |
| --- | --- | --- | --- | --- | --- | --- |
| TC01 | twoMinimalPositiveReturnsSum | (1, 1) | 2 | 2 | 通过 | 有效等价类 EC1（最小正整数） |
| TC02 | twoPositiveReturnsSum | (3, 5) | 8 | 8 | 通过 | 有效等价类 EC1 |
| TC03 | twoLargePositiveReturnsSum | (1234, 5678) | 6912 | 6912 | 通过 | 有效等价类 EC1 |
| TC04 | firstZeroSecondPositiveReturnsZero | (0, 5) | 0 | 5 | 失败 | 边界值（num1=0，<=0 上边界） |
| TC05 | firstPositiveSecondZeroReturnsZero | (5, 0) | 0 | 0 | 通过 | 边界值（num2=0） |
| TC06 | bothZeroReturnsZero | (0, 0) | 0 | 0 | 通过 | 边界值（双 0） |
| TC07 | firstNegativeSecondPositiveReturnsZero | (-1, 5) | 0 | 0 | 通过 | 无效等价类 EC2（num1<0） |
| TC08 | firstPositiveSecondNegativeReturnsZero | (5, -1) | 0 | 0 | 通过 | 无效等价类 EC2（num2<0） |
| TC09 | bothNegativeReturnsZero | (-1, -2) | 0 | 0 | 通过 | 无效等价类 EC2（双负） |

- 合计：9 条用例；通过 8、失败 1、错误 0、跳过 0。
- 说明：
  - 通过用例的“实际输出”由断言成功确认等于期望输出；失败用例 TC04 的“实际输出 = 5”来自 Surefire 失败信息 `expected: <0> but was: <5>`。
  - 本清单为独立设计，未参考任何已有测试或其他组的用例设计。
