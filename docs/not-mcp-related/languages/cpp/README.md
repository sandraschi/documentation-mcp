# C++ for Native Integration: The SOTA 2026 Standard

**Standard**: C++20/23 (Modern C++)
**Context**: The "Universal Solvent" of Computing
**Role**: Unreal Engine / Hardware Drivers / CUDA
**Build System**: CMake 3.25+
**Linting**: Clang-Tidy / Clang-Format

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for C++ usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity C++ Standard](#the-antigravity-c-standard)
    *   [Modern C++ (11 -> 20)](#modern-c-11---20)
    *   [RAII & Smart Pointers](#raii--smart-pointers)
    *   [The Rule of Zero](#the-rule-of-zero)
3.  [Global Context: C++ Evolution](#global-context-c-evolution)
    *   [History & Philosophy](#history--philosophy)
    *   [Design Principles](#design-principles)
    *   [The Standardization Era](#the-standardization-era)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Unreal Engine Integration](#unreal-engine-integration)
    *   [Hardware Abstraction (Unitree)](#hardware-abstraction-unitree)
    *   [Python Interop (`pybind11`)](#python-interop-pybind11)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Build Systems (CMake + Conan)](#build-systems-cmake--conan)
    *   [Templates & Metaprogramming](#templates--metaprogramming)
    *   [Concurrency (Std::Thread vs Asio)](#concurrency-stdthread-vs-asio)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, C++ is the **Native Bridge**. It connects our high-level logic (Python) to the deep metal of hardware (Robots, GPUs) and the virtual reality of game engines (Unreal).

**Why C++ for SOTA 2026?**
-   **Unreal Engine**: For Virtual Robotics, C++ is non-negotiable. Blueprints are for prototyping; C++ is for production MCP integration.
-   **Legacy Compatibility**: The world runs on C++. Drivers for LIDAR, Cameras, and Robot Arms are written in C/C++. We wrap them here.
-   **Performance**: While Rust is safer, C++ currently has the deepest ecosystem for high-performance computing (CUDA, TensorRT).

**The Pivot to Rust**:
*We explicitly prefer Rust for GREENFIELD native projects.* Use C++ only when integrating with existing C++ ecosystems (Unreal, specialized drivers).

---

## 2. The Antigravity C++ Standard

### Modern C++ (11 -> 20)

We strictly ban "C-style C++".
-   **No `new`/`delete`**: Manual memory management is forbidden.
-   **No `void*`**: Type safety is mandatory.
-   **No macros**: Use `constexpr` and `template` instead.

### RAII & Smart Pointers

**RAII (Resource Acquisition Is Initialization)** is the most important pattern in C++.
Resources (memory, file handles, sockets) are acquired in a constructor and released in a destructor.

**Standard Pointers:**
1.  `std::unique_ptr<T>`: The default. Sole ownership. Fast.
2.  `std::shared_ptr<T>`: Shared ownership via reference counting. Thread-safe control block.
3.  `std::weak_ptr<T>`: Non-owning reference to break cycles.

#### Code Example (SOTA 2026)

```cpp
#include <memory>
#include <vector>
#include <iostream>

class SensorDriver {
public:
    SensorDriver() { std::cout << "Sensor Initialized\n"; }
    ~SensorDriver() { std::cout << "Sensor Shutdown\n"; }
    void read() { /* ... */ }
};

void run_cycle() {
    // Unique pointer: Automatically deleted when out of scope
    auto sensor = std::make_unique<SensorDriver>(); 
    sensor->read();
    
    // No delete needed. No leaks possible.
}
```

### The Rule of Zero

If your class manages resources via smart pointers or standard containers (`std::vector`, `std::string`), you should **not** write a custom destructor, copy constructor, or assignment operator. The compiler generates them correctly.

---

## 3. Global Context: C++ Evolution

*(Ingested from Wikipedia Research)*

### History & Philosophy
C++ was developed by **Bjarne Stroustrup** at Bell Labs starting in 1979 as an extension of the C language. Originally named "C with Classes", it aimed to add object-oriented features (inspired by Simula) to C's speed and portability.

**Philosophy**:
-   *Trust the programmer.* (This is where C++ diverges from Rust).
-   *Don't pay for what you don't use.* (Zero-overhead principle).
-   *Compatibility with C.* (Almost any C program is a valid C++ program, historically).

### Design Principles
C++ is designed for:
-   **Systems Programming**: Operating systems, embedded systems, engines.
-   **Resource Constrained Environments**: Where every byte and cycle counts.
-   **Large Scale Software**: Encapsulation and modularity features were added to manage complexity (e.g., Namespaces).

### The Standardization Era
-   **C++98**: The first standard. Good for its time, but verbose.
-   **C++11**: "Modern C++". `auto`, lambdas, smart pointers, move semantics. Massive shift.
-   **C++14/17**: Refinements. `std::optional`, `std::variant`, file system.
-   **C++20**: Major leap. Concepts (constraints on templates), Modules (goodbye headers), Coroutines.

**In Antigravity, we target C++20.**

---

## 4. Fleet Integration Patterns

### Unreal Engine Integration

Unreal Engine (UE5) uses a customized C++ dialect (macros, garbage collection via `UObject`).

**Pattern: The MCP Subsystem**
We implement the MCP Server as a `UGameInstanceSubsystem`. This ensures it persists across level loads.

```cpp
// McpSubsystem.h
#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "McpSubsystem.generated.h"

UCLASS()
class MYGAME_API UMcpSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    
    UFUNCTION(BlueprintCallable)
    void SendMcpMessage(FString Message);
};
```

### Hardware Abstraction (Unitree)

Most robot SDKs provide a C++ header and a shared library (`.so`/`.dll`).
We wrap this in a Modern C++ class that handles the RAII lifecycle of the connection.

```cpp
// RobotWrapper.cpp
class RobotWrapper {
    UnitreeSafe* robot; // Hypothetical raw pointer from SDK
public:
    RobotWrapper() { robot = unitree_init(); }
    ~RobotWrapper() { unitree_free(robot); } // Safe cleanup
};
```

### Python Interop (`pybind11`)

When we need C++ speed in our Python agents, we use **pybind11**. It is a lightweight header-only library that exposes C++ types in Python.

```cpp
#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(fast_math, m) {
    m.doc() = "pybind11 example plugin"; 
    m.def("add", &add, "A function to add two numbers");
}
```

---

## 5. Advanced Patterns

### Build Systems (CMake + Conan)

**CMake** is the industry standard meta-build system.
**Conan** is the package manager (C++'s answer to `npm` or `cargo`).

**Standard `CMakeLists.txt`:**
```cmake
cmake_minimum_required(VERSION 3.25)
project(McpNative VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

add_library(mcp_native MODULE src/main.cpp)
target_link_libraries(mcp_native PRIVATE pybind11::module)
```

### Templates & Metaprogramming

Templates allow generic programming. In C++20, we use **Concepts** to constrain templates, making errors readable (finally!).

```cpp
template<typename T>
concept Number = std::integral<T> || std::floating_point<T>;

template<Number T>
T add(T a, T b) {
    return a + b;
}
```

### Concurrency (Std::Thread vs Asio)

-   **Simple Tasks**: `std::jthread` (C++20, auto-joining).
-   **High Performance**: `Boost.Asio` (async I/O similar to Python's asyncio).

---

## 6. Security Best Practices

1.  **Buffer Overflows**: Avoid `char*` and `strcpy`. Use `std::string`.
2.  **Dangling References**: Never return a reference to a local variable.
3.  **Thread Safety**: Use `std::mutex` and `std::lock_guard` (RAII locking). Never manually `lock()`/`unlock()`.

---

## 7. Reference Material

-   [CppReference (The Bible)](https://en.cppreference.com/w/)
-   [ISOCPP (The Standard)](https://isocpp.org/)
-   [Unreal Engine C++ API](https://docs.unrealengine.com/5.3/en-US/API/)
-   [CMake Documentation](https://cmake.org/documentation/)
-   [Pybind11 Documentation](https://pybind11.readthedocs.io/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
