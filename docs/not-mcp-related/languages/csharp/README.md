# C# for Simulation & Enterprise: The SOTA 2026 Standard

**Version**: .NET 8+ / C# 12+ (Mandatory)
**Context**: "Game Logic" & Enterprise Backends
**Role**: Virtual Robotics (Unity) / High-Throughput Servers
**Build System**: `dotnet` CLI / MSBuild
**Linting**: Roslyn Analyzers / StyleCop

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for C# usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity C# Standard](#the-antigravity-c-standard)
    *   [Modern C# (Records & Patterns)](#modern-c-records--patterns)
    *   [Async/Await (The Original)](#asyncawait-the-original)
    *   [Performance (`Span<T>`)](#performance-spant)
3.  [Global Context: C# Evolution](#global-context-c-evolution)
    *   [History & Philosophy](#history--philosophy)
    *   [Design Principles](#design-principles)
    *   [The .NET Core Revolution](#the-net-core-revolution)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Unity 6 Scripting (Virtual Robotics)](#unity-6-scripting-virtual-robotics)
    *   [MCP Servers (`mcp-sharp`)](#mcp-servers-mcp-sharp)
    *   [Dependency Injection](#dependency-injection)
5.  [Advanced Patterns](#advanced-patterns)
    *   [LINQ (Declarative Data)](#linq-declarative-data)
    *   [Source Generators](#source-generators)
    *   [Blazor (WebAssembly)](#blazor-webassembly)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, C# serves two distinct but critical roles:
1.  **Virtual Robotics**: It is the scripting language of Unity 6. All virtual robot logic (AI, pathfinding, interaction) runs on Mono/CoreCLR via C#.
2.  **Enterprise MCP Servers**: For integrating with Microsoft ecosystems (Azure, Office 365, Active Directory), a native .NET 8 MCP server is the most robust solution.

**Why C# for SOTA 2026?**
-   **Unity Dominance**: There is no alternative for Unity development.
-   **Productivity**: With Visual Studio 2022 / JetBrains Rider, the tooling (Intellisense, Refactoring) is superior to almost any other language.
-   **Performance**: .NET 8 rivals C++ and Rust in many benchmarks thanks to JIT optimization and `Span<T>`.

---

## 2. The Antigravity C# Standard

### Modern C# (Records & Patterns)

We ban "Java-style C#" (verbose getters/setters).
-   **Records**: Immutable data objects.
-   **Pattern Matching**: Concise switch expressions.
-   **Nullable Reference Types**: Compile-time null safety.

#### Code Example (SOTA 2026)

```csharp
// Models/RobotState.cs
public record RobotState(
    string Id,
    Vector3 Position,
    float BatteryLevel,
    bool IsActive
);

// Services/DecisionEngine.cs
public string DecideAction(RobotState state) => state switch
{
    { BatteryLevel: < 0.1f } => "ReturnToCharger",
    { IsActive: false } => "WakeUp",
    _ => "Patrol"
};
```

### Async/Await (The Original)

C# pioneered the `async`/`await` pattern adopted by Python and JS.
**Rule**: All I/O must be async. Use `Task`, `ValueTask`, and `CancellationToken`.

```csharp
public async Task<string> FetchDataAsync(string url, CancellationToken ct)
{
    using var client = new HttpClient();
    var response = await client.GetAsync(url, ct);
    return await response.Content.ReadAsStringAsync(ct);
}
```

### Performance (`Span<T>`)

For high-performance code (e.g., parsing binary data from a Lidar stream), we use `Span<T>` and `Memory<T>` to slice arrays without allocating new memory.

```csharp
public void ProcessStream(ReadOnlySpan<byte> data)
{
    var header = data.Slice(0, 4); // Zero allocation
    var payload = data.Slice(4);   // Zero allocation
}
```

---

## 3. Global Context: C# Evolution

*(Ingested from Wikipedia Research)*

### History & Philosophy
C# was developed by **Anders Hejlsberg** (creator of Turbo Pascal and Delphi) at Microsoft. It was announced in 2000 as part of the .NET initiative.
-   **Cool (C-like Object Oriented Language)**: The internal codename.
-   **Java Clone?**: Originally criticized as a Java clone, C# rapidly diverged with features like properties, events, and reified generics.

**Evolution**:
-   **C# 2.0 (2005)**: Generics. (Superior to Java's type erasure).
-   **C# 3.0 (2007)**: LINQ and Lambda Expressions. (Functional programming enters the mainstream).
-   **C# 5.0 (2012)**: Async/Await. (Revolutionized concurrency).
-   **C# 9.0+**: Records, Init-only setters, Top-level statements.

### Design Principles
C# is a **multi-paradigm** language:
-   **Strong Typing**: Statically typed.
-   **Imperative**: Structured programming.
-   **Declarative**: LINQ.
-   **Functional**: Lambdas, pattern matching, immutability.
-   **Generic**: Reified generics.
-   **Object-Oriented**: Class-based.

### The .NET Core Revolution
Microsoft rebooted the ecosystem with **.NET Core** (now just **.NET 5+**). It is open-source, cross-platform (Linux/macOS), and modular.
This allows us to run C# MCP servers in Docker containers alongside Python/Rust services.

---

## 4. Fleet Integration Patterns

### Unity 6 Scripting (Virtual Robotics)

In Unity, C# scripts define the behavior of `GameObjects`.
For MCP integration, we use a `MonoBehaviour` that listens to OSC messages or HTTP requests.

```csharp
using UnityEngine;
using Unitree.Robotics;

public class VirtualGo2 : MonoBehaviour
{
    [SerializeField] private float speed = 2.0f;
    private Rigidbody rb;
    
    void Start() { rb = GetComponent<Rigidbody>(); }
    
    // Called by MCP via UnityEvent or Reflection
    public void Move(Vector3 direction)
    {
        rb.AddForce(direction * speed);
    }
}
```

### MCP Servers (`mcp-sharp`)

We use the official/community C# SDK for standard MCP servers.
ASP.NET Core Minimal APIs are the preferred host.

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/mcp/tools", () => 
{
    return new[] { new Tool("get_weather", "Get weather info") };
});

app.Run();
```

### Dependency Injection

.NET has a world-class DI container built-in. Use it.
**Constructor Injection** is the standard.

```csharp
public class RobotController
{
    private readonly IRobotInterface _robot;
    private readonly ILogger<RobotController> _logger;
    
    public RobotController(IRobotInterface robot, ILogger<RobotController> logger)
    {
        _robot = robot;
        _logger = logger;
    }
}
```

---

## 5. Advanced Patterns

### LINQ (Declarative Data)

LINQ (Language Integrated Query) allows querying collections like SQL.
In SOTA 2026, we use method syntax (`.Where()`) over query syntax (`from x in ...`).

```csharp
var activeRobots = robots
    .Where(r => r.IsActive)
    .OrderByDescending(r => r.BatteryLevel)
    .Select(r => r.Name)
    .ToList();
```

### Source Generators

C# allows generating code at compile time. We use this for:
-   **JSON Serialization**: `System.Text.Json` source generator (avoids reflection).
-   **Logging**: `LoggerMessage` generator (high performance).

### Blazor (WebAssembly)

For internal dashboards, we sometimes use Blazor functionality to run C# in the browser, sharing DTOs with the backend.

---

## 6. Security Best Practices

1.  **Roslyn Analyzers**: Enable all security rules (`Microsoft.CodeAnalysis.NetAnalyzers`).
2.  **Secrets**: Use `dotnet user-secrets` for dev, Azure Key Vault for prod.
3.  **Validation**: Use `FluentValidation` for robust input checking.

---

## 7. Reference Material

-   [Microsoft C# Documentation](https://learn.microsoft.com/en-us/dotnet/csharp/)
-   [.NET 8 Overview](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8)
-   [Unity Scripting API](https://docs.unity3d.com/ScriptReference/)
-   [LINQ 101 Samples](https://linqsamples.com/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
