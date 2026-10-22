package com.example.lab2;

import java.util.Objects;

/** Independent non-JUnit execution used only to record actual Java results.
 *  Do not present these results as a JUnit 5 / Maven run.
 */
public class ChatGPTLab2JavaVerifier {
    private record Case(String id, int x, int y, int z, int expected) {}
    public static void main(String[] args) {
        Case[] cases = {
            new Case("TC01", 3, 0, 5, 11),
            new Case("TC02", 6, 1, 6, 1),
            new Case("TC03", 2, 1, 6, 2),
            new Case("TC04", 6, 0, 6, 12),
            new Case("TC05", 2, 0, 5, 2),
            new Case("TC06", 3, 0, 6, 12),
            new Case("TC07", 3, 1, 5, 3)
        };
        Calculator subject = new Calculator();
        int passed = 0;
        for (Case c : cases) {
            int actual = subject.Example(c.x(), c.y(), c.z());
            boolean ok = actual == c.expected();
            if (ok) passed++;
            System.out.printf("%s | input=(%d,%d,%d) | expected=%d | actual=%d | %s%n",
                c.id(), c.x(), c.y(), c.z(), c.expected(), actual, ok ? "PASS" : "FAIL");
        }
        System.out.printf("RESULT | executed=%d | passed=%d | failed=%d%n", cases.length, passed, cases.length - passed);
        if (passed != cases.length) System.exit(1);
    }
}
