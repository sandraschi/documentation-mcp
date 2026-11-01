---
title: "Fleet Development Terms & Concepts Encyclopedia"
category: reference
status: active
audience: fleet
last_updated: 2026-09-12
---

# Fleet Development Terms & Concepts Encyclopedia

A comprehensive conceptual reference for software engineering, architecture, and testing patterns across the 200+ repository fleet.

---

## Core Software Engineering & Runtime Concepts

### Monkeypatching

**Definition**: The runtime modification of a class, module, method, or function without altering the underlying source code on disk. In dynamic languages like Python, this is accomplished by rebinding attributes on module or class namespaces (e.g. `module.target_func = replacement_func`), using object proxies (such as `wrapt.ObjectProxy`), or attaching call-site wrappers (`wrapture.binding`).

#### Mechanics & Implementations
1. **Direct Namespace Rebinding (`setattr` / assignment)**:  
   Directly replacing a function or method reference in a module or class dictionary. The simplest approach, but vulnerable to import-order races (if another module already did `from module import target_func`, the binding remains unchanged in that module).
2. **Proxy Decorators (`wrapt`)**:  
   Wraps functions and classes transparently while preserving signatures, docstrings, and introspection, avoiding standard `functools.wraps` edge cases.
3. **Call-Site & AST Interception (`wrapture`, bytecode rewrites)**:  
   Attaches bindings at specific call sites, intercepting arguments, stubbing return values, or injecting exceptions without mutating the target module's global definition.
4. **Scoped Fixtures (`unittest.mock.patch`, `monkeypatch` in pytest)**:  
   Applies patches strictly within the lifespan of a test case or context manager and guarantees teardown restoration.

#### Fleet Policy: The Production vs Testing Divide

```
                     ┌──────────────────────────────────────────────┐
                     │              MONKEYPATCHING                  │
                     └──────────────────────┬───────────────────────┘
                                            │
                   ┌────────────────────────┴────────────────────────┐
                   │                                                 │
                   ▼                                                 ▼
        [ PRODUCTION MCP CODE ]                            [ TESTS & DIAGNOSTICS ]
          STATUS: PROHIBITED                                 STATUS: APPROVED
     - Breaks static typing (ruff/ty)                   - Stubs un-injectable C-extensions
     - Non-deterministic import races                   - Deterministic fault injection
     - Leaks state across async loops                   - Ad-hoc hang/deadlock capture
     - Corrupts stdio / wire protocols                  - Replaces brittle spec-less mocks
```

* **Production Servers**: **Strictly Prohibited.** FastMCP servers must never monkeypatch standard libraries, third-party frameworks, or other fleet modules at runtime. It destroys debuggability, causes race conditions in async event loops, and violates the MCP First-Time-Success Guarantee.
* **Testing & Diagnostics**: **Encouraged & Surgical.** Ideal for:
  - Mocking native Windows C-extensions and Win32 APIs (e.g. `win32file`, `win32security` in `windows-operations-mcp`) where dependency injection is impossible.
  - Fault injection testing (e.g. simulating HTTP timeouts, socket resets, or SMTP disconnects in `email-mcp`).
  - Ad-hoc deadlock inspection via tools like `wrapture` or `py-spy` without modifying repository code.

---

### Call-Site Interception

**Definition**: A fine-grained form of runtime observation where behavior is attached to the *caller's invocation* of a function rather than mutating the callee itself. Unlike global namespace monkeypatching, call-site interception allows observing or altering interactions between specific components while leaving the rest of the runtime unaffected.

---

### Mocks vs Stubs vs Spies vs Dynamic Bindings

| Concept | Purpose | When to Use in Fleet |
|---|---|---|
| **Stub** | Returns canned, predefined responses without asserting on how it was invoked. | Unit tests where external dependencies (e.g. a weather API) need fixed test data. |
| **Mock** | Pre-programmed with expectations about calls it should receive (count, arguments). | Verifying that side-effects occurred (e.g. checking that an email dispatch was triggered). |
| **Spy** | Wraps a real object to record invocations while allowing the original implementation to execute. | Testing integration boundaries without altering behavior. |
| **Dynamic Binding (`wrapture`)** | Attaches transparently to real code call sites, recording call trees and allowing selective intervention (stubbing, fault injection) on real objects. | Native Win32/WMI boundary tests where mocking C-extensions is otherwise brittle. |

---

### Structured Logging (`structlog`) vs Distributed Tracing (OpenTelemetry)

* **Structured Logging**: Emits machine-readable, contextual JSON events (key-value pairs) per operation. Critical for stdio MCP servers where log streams must strictly bypass stdout to prevent protocol framing corruption.
* **Distributed Tracing (OTel)**: Correlates operations across service boundaries via trace and span IDs (`traceparent`). High-value for HTTP/SSE gateways (`observability-mcp`, `meta-mcp`), but heavy overhead for short-lived, single-purpose stdio MCP tools.
