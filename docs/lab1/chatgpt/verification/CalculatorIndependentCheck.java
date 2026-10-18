package study.myconnect.cn;

/** 无第三方依赖的执行器。注意：本程序不是 JUnit 引擎。 */
public class CalculatorIndependentCheck {
    record Case(String id, String method, int a, int b, int expected) {}
    public static void main(String[] args) {
        Calculator calculator = new Calculator();
        Case[] cases = {
            new Case("TC01", "positiveSmall", 1, 2, 3),
            new Case("TC02", "positiveMedium", 4, 5, 9),
            new Case("TC03", "firstZeroSecondOne", 0, 1, 0),
            new Case("TC04", "firstZeroSecondSeven", 0, 7, 0),
            new Case("TC05", "secondZero", 1, 0, 0),
            new Case("TC06", "bothZero", 0, 0, 0),
            new Case("TC07", "firstNegative", -1, 2, 0),
            new Case("TC08", "secondNegative", 2, -1, 0),
            new Case("TC09", "bothNegative", -1, -1, 0),
            new Case("TC10", "negativeAndZero", -1, 0, 0),
            new Case("TC11", "zeroAndNegative", 0, -1, 0),
            new Case("TC12", "positiveLarger", 10, 20, 30)
        };
        int failures = 0;
        System.out.println("JAVA DIRECT-CALL CHECK (NOT JUNIT)");
        System.out.println("id,method,input,expected,actual,result");
        for (Case c : cases) {
            int actual = calculator.add(c.a(), c.b());
            boolean pass = actual == c.expected();
            if (!pass) failures++;
            System.out.printf("%s,%s,\"(%d,%d)\",%d,%d,%s%n",
                c.id(), c.method(), c.a(), c.b(), c.expected(), actual, pass ? "PASS" : "FAIL");
        }
        System.out.printf("SUMMARY: tests=%d, passed=%d, failed=%d%n", cases.length, cases.length - failures, failures);
        if (failures != 0) System.exit(1);
    }
}
