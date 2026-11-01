# Julia for Scientific Computing: The SOTA 2026 Standard

**Standard**: Julia 1.10+ (Mandatory)
**Context**: "Walks like Python, Runs like C"
**Role**: Theoretical Physics / Simulation Modeling / Optimization
**Build System**: `Pkg.jl`
**Linting**: `JuliaFormatter`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Julia usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Julia Standard](#the-antigravity-julia-standard)
    *   [Multiple Dispatch (The Core)](#multiple-dispatch-the-core)
    *   [Type System (Just-In-Time)](#type-system-just-in-time)
    *   [Broadcasting (Dot Syntax)](#broadcasting-dot-syntax)
3.  [Global Context: Julia Evolution](#global-context-julia-evolution)
    *   [History: The "Greedy" Language (2012)](#history-the-greedy-language-2012)
    *   [The Two-Language Problem](#the-two-language-problem)
    *   [DifferentialEquations.jl](#differentialequationsjl)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Trajectory Optimization](#trajectory-optimization)
    *   [Model Predictive Control (MPC)](#model-predictive-control-mpc)
    *   [Data Analysis Notebooks (Pluto.jl)](#data-analysis-notebooks-plutojl)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Metaprogramming (Generated Functions)](#metaprogramming-generated-functions)
    *   [GPU Programming (`CUDA.jl`)](#gpu-programming-cudajl)
    *   [Automatic Differentiation (Zygote/Enzyme)](#automatic-differentiation-zygoteenzyme)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Julia is the **Brain**.
When we need to calculate an optimal trajectory for a quadruped across 10 seconds of rough terrain, involving 12,000 interlocking differential equations, Python chokes. C++ takes a week to write.
Julia solves it in 50ms (Model Predictive Control).

**Why Julia for SOTA 2026?**
-   **Speed**: LLVM-based JIT compilation means it runs at C speeds.
-   **Math**: First-class support for linear algebra, matrices, and complex numbers.
-   **Composability**: Packages work together magically due to multiple dispatch (e.g., Automatic Differentiation works on DifferentialEquations solvers instantly).

---

## 2. The Antigravity Julia Standard

### Multiple Dispatch (The Core)

In most OOP languages, `object.method()` happens.
In Julia, `function(arg1, arg2)` selects the most specific method based on **ALL** argument types.

```julia
collide(x::Asteroid, y::Asteroid) = ...
collide(x::Asteroid, y::Spaceship) = ...
collide(x::Spaceship, y::Asteroid) = ...
collide(x::Spaceship, y::Spaceship) = ...
```
This is fundamental to how the ecosystem composes.

### Type System (Just-In-Time)

Types are dynamic but can be annotated for performance and clarity.
If the compiler can infer the type, it generates optimized machine code.

```julia
function add_vectors(a::Vector{Float64}, b::Vector{Float64})
    return a + b
end
```

### Broadcasting (Dot Syntax)

Apply any function element-wise by adding a dot. No more loops.

```julia
A = [1, 2, 3]
B = sin.(A) .+ 5  # sin(1)+5, sin(2)+5, sin(3)+5
```

---

## 3. Global Context: Julia Evolution

*(Ingested from Wikipedia Research)*

### History: The "Greedy" Language (2012)
Created at **MIT** by **Jeff Bezanson**, **Stefan Karpinski**, **Viral B. Shah**, and **Alan Edelman**.
They wanted: C speed, Python dynamism, Lisp macros, Matlab math. They were greedy. They succeeded.

### The Two-Language Problem
Before Julia, you prototyped in Python/Matlab (slow, easy) and rewrote in C++/Fortran (fast, hard).
Julia solves this: You prototype in Julia, and then you... optimize your Julia code slightly. One language.

### DifferentialEquations.jl
The killer app. Widely considered the best differential equation solver suite in any language. It solves ODEs, SDEs, DDEs, DAEs.

---

## 4. Fleet Integration Patterns

### Trajectory Optimization

We define the robot's capabilities (torque limits, mass) and the terrain.
We solve the optimization problem (minimize energy) in real-time on the robot's onboard GPU.

### Model Predictive Control (MPC)

Predicting the next 100 steps of the robot, executing the first step, and re-predicting.
Julia's low latency makes this feasible at 50Hz.

### Data Analysis Notebooks (Pluto.jl)

Unlike Jupyter, **Pluto.jl** notebooks are reactive. Changing code in one cell updates dependent cells instantly. It is reproducible science.

---

## 5. Advanced Patterns

### Metaprogramming (Generated Functions)

Writing code that writes code based on types.
Used to unroll loops for small matrices (StaticArrays.jl).

### GPU Programming (`CUDA.jl`)

Write Julia code, run it on NVIDIA GPUs.
`CuArray(A) * CuArray(B)` happens on the GPU. No C++ CUDA required.

### Automatic Differentiation (Zygote/Enzyme)

Julia can take the derivative of *arbitrary code* (including loops and conditionals).
This is essential for training neural networks (Flux.jl) and physics-informed ML.

---

## 6. Security Best Practices

1.  **Code Loading**: Be careful with `include()`. Julia executes code at the top level.
2.  **Manifest.toml**: Always commit the Manifest to ensure reproducible environments.

---

## 7. Reference Material

-   [Julia Documentation](https://docs.julialang.org/)
-   [JuliaHub](https://juliahub.com/)
-   [SciML (Scientific Machine Learning)](https://sciml.ai/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
