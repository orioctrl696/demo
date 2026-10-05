package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ApplicationTest {
    @Test
    void greetsNamedUser() {
        assertEquals("Hello, Java!", Application.greeting("Java"));
    }

    @Test
    void usesDefaultGreetingForBlankName() {
        assertEquals("Hello, World!", Application.greeting("  "));
    }
}
