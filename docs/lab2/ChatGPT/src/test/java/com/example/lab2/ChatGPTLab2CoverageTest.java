package com.example.lab2;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

/** ChatGPT-designed Lab2 tests: decision / statement / condition / C-D coverage. */
public class ChatGPTLab2CoverageTest {
    private final Calculator calculator = new Calculator();

    // Core coverage set: TC01 + TC02 + TC03.
    @Test
    void tc01_bothDecisionsTrue() {
        assertEquals(11, calculator.Example(3, 0, 5));
    }

    @Test
    void tc02_bothDecisionsFalse() {
        assertEquals(1, calculator.Example(6, 1, 6));
    }

    @Test
    void tc03_shortCircuitAndOrRightTrue() {
        assertEquals(2, calculator.Example(2, 1, 6));
    }

    // Supplementary cases: branch combinations and boundary behavior.
    @Test
    void tc04_firstTrueSecondFalse() {
        assertEquals(12, calculator.Example(6, 0, 6));
    }

    @Test
    void tc05_xBelowThreeAndZAtFive() {
        assertEquals(2, calculator.Example(2, 0, 5));
    }

    @Test
    void tc06_firstTrueAndSecondTrueViaRightOperand() {
        assertEquals(12, calculator.Example(3, 0, 6));
    }

    @Test
    void tc07_firstFalseViaYAndSecondTrue() {
        assertEquals(3, calculator.Example(3, 1, 5));
    }
}
