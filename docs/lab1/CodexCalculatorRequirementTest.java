package com.example.lab1;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CodexCalculatorRequirementTest {
    @ParameterizedTest(name = "{0}: add({1}, {2}) should return {3}")
    @CsvSource({
            "P01, 1, 1, 2",
            "P02, 2, 3, 5",
            "P03, 3, 2, 5",
            "P04, 1000000000, 1000000000, 2000000000",
            "Z01, 0, 1, 0",
            "Z02, 1, 0, 0",
            "Z03, 0, 0, 0",
            "N01, -1, 1, 0",
            "N02, 1, -1, 0",
            "N03, -1, 0, 0",
            "N04, 0, -1, 0",
            "N05, -1, -1, 0"
    })
    void addFollowsRequirement(String caseId, int num1, int num2, int expected) {
        assertEquals(expected, new Calculator().add(num1, num2), caseId);
    }
}
