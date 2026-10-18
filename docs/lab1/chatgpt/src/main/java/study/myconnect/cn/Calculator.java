package study.myconnect.cn;

// 原始题目代码：保留故意引入的 >= 缺陷，不做修复。
public class Calculator {
    public int add(int num1, int num2) {
        if (num1 >= 0 && num2 > 0) {
            return num1 + num2;
        } else {
            return 0;
        }
    }
}
