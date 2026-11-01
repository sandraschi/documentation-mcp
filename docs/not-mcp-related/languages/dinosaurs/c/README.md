# C: The Lingua Franca

**Standard**: C17 / C23 (Mandatory)
**Context**: "Portable Assembly"
**Role**: Kernels / Python Interpreters / Embedded Firmware
**Build System**: `cmake` / `make`
**Linting**: `clang-tidy` / `cppcheck`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for C usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity C Standard](#the-antigravity-c-standard)
    *   [Memory Management (Manual)](#memory-management-manual)
    *   [Undefined Behavior (The Dragon)](#undefined-behavior-the-dragon)
    *   [Pointers & Arrays](#pointers--arrays)
3.  [Global Context: C Evolution](#global-context-c-evolution)
    *   [History: Dennis Ritchie & Unix (1972)](#history-dennis-ritchie--unix-1972)
    *   [K&R vs ANSI C](#kr-vs-ansi-c)
    *   [C11/C17/C23](#c11c17c23)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [CPython Extensions](#cpython-extensions)
    *   [Embedded Systems (FreeRTOS)](#embedded-systems-freertos)
    *   [Linux Kernel Modules](#linux-kernel-modules)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Macros (The Preprocessor)](#macros-the-preprocessor)
    *   [`void*` Polymorphism](#void-polymorphism)
    *   [`stdatomic.h` (Concurrency)](#stdatomich-concurrency)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, C is the **Foundation**.
Python is written in C. The Linux Kernel is written in C. Git is written in C.
We respect C because it is the language of our tools.

**Why C for SOTA 2026?**
-   **Portability**: If a CPU exists, there is a C compiler for it.
-   **ABI Stability**: The C ABI (Application Binary Interface) is the universal protocol for libraries to talk to each other (Rust <-> C <-> Python).
-   **Simplicity**: It fits in your head (mostly).

---

## 2. The Antigravity C Standard

### Memory Management (Manual)

`malloc` and `free`.
**Rule**: Every `malloc` must have a matching `free`. Use AddressSanitizer (ASan) to enforce this.

```c
int *array = malloc(10 * sizeof(int));
if (!array) {
    perror("malloc failed");
    exit(1);
}
// ... use array ...
free(array);
```

### Undefined Behavior (The Dragon)

C assumes you know what you are doing.
-   Signed integer overflow? UB.
-   Dereferencing null? UB.
-   Shifting by 32? UB.

**Rule**: We compile with `-Wall -Wextra -Werror -fsanitize=undefined`.

### Pointers & Arrays

In C, arrays decay to pointers. Understanding pointer arithmetic is mandatory.

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;
printf("%d", *(p + 2)); // prints 3
```

---

## 3. Global Context: C Evolution

*(Ingested from Wikipedia Research)*

### History: Dennis Ritchie & Unix (1972)
Created at **Bell Labs** by **Dennis Ritchie** to re-implement the Unix operating system (originally in Assembly).
It was derived from B (Ken Thompson), which was derived from BCPL.

### K&R vs ANSI C
-   **K&R (1978)**: The original informal spec ("The C Programming Language" book).
-   **ANSI C (C89/C90)**: The first official standard. Function prototypes introduced.

### C11/C17/C23
-   **C11**: Multi-threading support (`threads.h`, `stdatomic.h`), anonymous structs.
-   **C17**: Bug fix release.
-   **C23**: `true`/`false` keywords, `typeof`, `constexpr`, bit-precise integers.

---

## 4. Fleet Integration Patterns

### CPython Extensions

When Python is too slow, we write a C extension.
Modern SOTA: We treat Rust/PyO3 as the default, but C is fallback for legacy codebases.

### Embedded Systems (FreeRTOS)

For the motor controllers on our robots, we use C.
Low-level register access and deterministic timing are required.

```c
volatile uint32_t *GPIO_CRL = (uint32_t *)0x40010800;
*GPIO_CRL |= 0x01; // Set bit 0
```

### Linux Kernel Modules

Drivers for our custom hardware sensors (LIDAR interface) are written in C as kernel modules (`.ko`).

---

## 5. Advanced Patterns

### Macros (The Preprocessor)

The C Preprocessor is a text substitution tool.
We use it for conditional compilation (`#ifdef`) and generic-like behavior (X-Macros).

```c
#define MAX(a,b) ((a) > (b) ? (a) : (b))
```
*Warning: Double evaluation risk.*

### `void*` Polymorphism

Generic containers in C use `void*`.

```c
void qsort(void *base, size_t nitems, size_t size, 
           int (*compar)(const void *, const void*));
```

### `stdatomic.h` (Concurrency)

Lock-free programming using atomic primitives.

```c
atomic_int counter = ATOMIC_VAR_INIT(0);
atomic_fetch_add(&counter, 1);
```

---

## 6. Security Best Practices

1.  **Buffer Overflows**: Never use `gets`, `strcpy`, `strcat`. Use `fgets`, `strncpy`, `strncat`.
2.  **Format Strings**: Never pass user input as the format string to `printf`. `printf("%s", user_input)`.
3.  **Static Analysis**: Run `clang-tidy` in CI.

---

## 7. Reference Material

-   [The C Programming Language (K&R)](https://en.wikipedia.org/wiki/The_C_Programming_Language)
-   [C Reference (cppreference)](https://en.cppreference.com/w/c)
-   [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
