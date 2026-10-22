package com.example.lab2;

/** The method body is transcribed without alteration from the user's Lab2 screenshot.
 *  Package/class wrapper is added so that it compiles in a Maven Java project.
 */
public class Calculator {
    public int Example(int x, int y, int z) {
        int result = 0;
        if (x >= 3 && y == 0) {
            result = z + x;
        }
        if (z <= 5 || x < z) {
            result = result + x;
        } else {
            result = result + y;
        }
        return result;
    }
}
