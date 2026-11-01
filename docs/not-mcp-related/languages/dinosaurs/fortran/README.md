# Fortran for Numerical Legacy: The SOTA 2026 Standard

**Standard**: Fortran 2018+ (Mandatory)
**Context**: "Formula Translation"
**Role**: Legacy Physics / Weather Simulation / Linear Algebra
**Build System**: `fpm` (Fortran Package Manager) / CMake
**Linting**: `gfortran -Wall`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Fortran usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Fortran Standard](#the-antigravity-fortran-standard)
    *   [Arrays: The First-Class Citizen](#arrays-the-first-class-citizen)
    *   [Modules & Encapsulation](#modules--encapsulation)
    *   [C Interoperability (`iso_c_binding`)](#c-interoperability-iso_c_binding)
3.  [Global Context: Fortran Evolution](#global-context-fortran-evolution)
    *   [History: John Backus & IBM (1954)](#history-john-backus--ibm-1954)
    *   [The Evolution (77 -> 90 -> 2018)](#the-evolution-77---90---2018)
    *   [Why It Works (Aliasing)](#why-it-works-aliasing)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Legacy Physics Engines](#legacy-physics-engines)
    *   [High-Performance Computing (HPC)](#high-performance-computing-hpc)
    *   [Python Bindings (`f2py`)](#python-bindings-f2py)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Coarrays (Thinking in Parallel)](#coarrays-thinking-in-parallel)
    *   [Object-Oriented Fortran (Yes, Really)](#object-oriented-fortran-yes-really)
    *   [Pure Procedures](#pure-procedures)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Fortran is the **Old God**. We generally don't write *new* code in Fortran, but we respect and integrate with the mountains of battle-tested code that already exist (OpenFast for wind turbines, NASA orbital mechanics).

**Why Fortran for SOTA 2026?**
-   **Aliasing**: In C/C++, pointers can point to the same memory, limiting compiler optimization. In Fortran, arrays are unique. This makes it faster for matrix multiplication.
-   **Syntax**: `A = B + C` acts on entire arrays. It reads like math.
-   **Legacy**: If you want to simulate fluid dynamics, the best code was written in 1980.

---

## 2. The Antigravity Fortran Standard

### Arrays: The First-Class Citizen

Arrays are 1-based by default (like matrices in math).
Operations are element-wise.

```fortran
program matrix_add
    implicit none
    real, dimension(3,3) :: A, B, C
    
    A = 1.0
    B = 2.0
    
    ! Whole array operation
    C = A + B
    
    print *, C(1,1) ! Output: 3.0
end program matrix_add
```

### Modules & Encapsulation

We ban "Common Blocks" (global state from 77).
Use **Modules** to group data and functions.

```fortran
module physics_constants
    implicit none
    real, parameter :: G = 9.81
    real, parameter :: PI = 3.14159
end module

program fall
    use physics_constants
    print *, "Gravity is", G
end program
```

### C Interoperability (`iso_c_binding`)

We use the standard `iso_c_binding` module to call C functions or be called by C/Python.

```fortran
module c_interface
    use iso_c_binding
    implicit none
contains
    subroutine print_c(i) bind(c, name="print_fortran")
        integer(c_int), value :: i
        print *, "From C:", i
    end subroutine
end module
```

---

## 3. Global Context: Fortran Evolution

*(Ingested from Wikipedia Research)*

### History: John Backus & IBM (1954)
Fortran (The IBM Mathematical **For**mula **Tran**slating System) was the first widely used high-level language.
Before Fortran, programming was done in assembly.
**The Goal**: Make programming accessible to scientists/engineers, not just machine experts.

### The Evolution (77 -> 90 -> 2018)
-   **Fortran 77**: The fixed-format punched card standard. Still seen in extremely old libraries.
-   **Fortran 90**: Massive update. Free format, modules, recursive functions, dynamic memory.
-   **Fortran 2003**: Object-Oriented Programming (Classes/Inheritance).
-   **Fortran 2008/2018**: Coarrays (PGAS parallel model).

### Why It Works (Aliasing)
Fortran assumes that arguments to a function do not overlap in memory. This allows the compiler to vectorize loops extremely aggressively (SIMD instructions) without runtime checks. This is why BLAS/LAPACK (Linear Algebra) are still essentially Fortran under the hood.

---

## 4. Fleet Integration Patterns

### Legacy Physics Engines

For our **Unitree B2** robot (the heavy lifter), we use legacy simulation code for terrain analysis. This code is wrapped in a Python interface using `f2py` (part of NumPy).

### High-Performance Computing (HPC)

When running simulations on our cluster, we use MPI (Message Passing Interface). Fortran's MPI bindings are first-class.

### Python Bindings (`f2py`)

The easiest way to call Fortran from Python.

```bash
python -m numpy.f2py -c -m myphysics physics.f90
```
*Result: `import myphysics` works instantly.*

---

## 5. Advanced Patterns

### Coarrays (Thinking in Parallel)

Fortran 2008 introduced parallel syntax directly into the language.
`A[i]` accesses array `A` on image (processor) `i`.

```fortran
program hello_image
    implicit none
    print *, "Hello from image", this_image(), "of", num_images()
end program
```

### Object-Oriented Fortran (Yes, Really)

Since 2003, we can have classes and polymorphism.

```fortran
type :: Shape
contains
    procedure :: area
end type Shape

type, extends(Shape) :: Circle
    real :: radius
contains
    procedure :: area => circle_area
end type Circle
```

### Pure Procedures

Marking a function as `pure` guarantees no side effects. This allows the compiler to parallelize it automatically within `do concurrent` loops.

---

## 6. Security Best Practices

1.  **Implicit None**: ALWAYS use `implicit none`. By default, variables starting with I-N are integers. This causes silent bugs.
2.  **Bounds Checking**: Compile with `-fcheck=bounds` (gfortran) during development to catch memory errors.
3.  **Allocatable**: Use `allocatable` arrays instead of manual pointers (`pointer`) to prevent leaks.

---

## 7. Reference Material

-   [Fortran-lang.org](https://fortran-lang.org/) (The modern community site)
-   [Fortran Wiki](http://fortranwiki.org/)
-   [Modern Fortran via Examples](https://github.com/modern-fortran/modern-fortran)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
