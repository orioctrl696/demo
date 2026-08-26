package com.example.demo;

public final class Application {
    private Application() {
    }

    public static String greeting(String name) {
        if (name == null || name.isBlank()) {
            return "Hello, World!";
        }
        return "Hello, " + name.trim() + "!";
    }

    public static void main(String[] args) {
        String name = args.length == 0 ? "World" : String.join(" ", args);
        System.out.println(greeting(name));
    }
}
