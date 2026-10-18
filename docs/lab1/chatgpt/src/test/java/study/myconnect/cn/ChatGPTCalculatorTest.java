package study.myconnect.cn;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

/** 按功能需求设计；不改变 Calculator.java。 */
public class ChatGPTCalculatorTest {
    private final Calculator calculator = new Calculator();

    @Test void positiveSmall() { assertEquals(3, calculator.add(1, 2)); }
    @Test void positiveMedium() { assertEquals(9, calculator.add(4, 5)); }
    @Test void firstZeroSecondOne() { assertEquals(0, calculator.add(0, 1)); }
    @Test void firstZeroSecondSeven() { assertEquals(0, calculator.add(0, 7)); }
    @Test void secondZero() { assertEquals(0, calculator.add(1, 0)); }
    @Test void bothZero() { assertEquals(0, calculator.add(0, 0)); }
    @Test void firstNegative() { assertEquals(0, calculator.add(-1, 2)); }
    @Test void secondNegative() { assertEquals(0, calculator.add(2, -1)); }
    @Test void bothNegative() { assertEquals(0, calculator.add(-1, -1)); }
    @Test void negativeAndZero() { assertEquals(0, calculator.add(-1, 0)); }
    @Test void zeroAndNegative() { assertEquals(0, calculator.add(0, -1)); }
    @Test void positiveLarger() { assertEquals(30, calculator.add(10, 20)); }
}
