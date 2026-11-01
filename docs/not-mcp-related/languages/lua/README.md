# Lua for Embedded Configuration: The SOTA 2026 Standard

**Standard**: LuaJIT (Neovim/Nginx) / Lua 5.4 (Redis)
**Context**: "Mechanisms, not Policies"
**Role**: Editor Configuration / Game Scripting / Redis Atoms
**Build System**: `luarocks`
**Linting**: `luacheck`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Lua usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Lua Standard](#the-antigravity-lua-standard)
    *   [Tables: The Universal Structure](#tables-the-universal-structure)
    *   [Metatables & OOP](#metatables--oop)
    *   [Coroutines (Cooperative Multitasking)](#coroutines-cooperative-multitasking)
3.  [Global Context: Lua Evolution](#global-context-lua-evolution)
    *   [History & Philosophy (Brazil 1993)](#history--philosophy-brazil-1993)
    *   [LuaJIT: The Speed Demon](#luajit-the-speed-demon)
    *   [Embeddability](#embeddability)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Neovim Configuration (`init.lua`)](#neovim-configuration-initlua)
    *   [Redis Scripting (Atomic Logic)](#redis-scripting-atomic-logic)
    *   [Nginx/OpenResty](#nginxopenresty)
5.  [Advanced Patterns](#advanced-patterns)
    *   [FFI (Foreign Function Interface)](#ffi-foreign-function-interface)
    *   [Sandboxing (`setfenv`/`_ENV`)](#sandboxing-setfenv_env)
    *   [Iterators & Closures](#iterators--closures)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Lua is the **Configuration Engine**. It is small, fast, and exists where Python is too heavy and JSON is too static.

**Why Lua for SOTA 2026?**
-   **Neovim**: Our editor of choice is built on LuaJIT. Proficiency in Lua means proficiency in your IDE.
-   **Redis**: We execute complex atomic transactions on the database server using Lua scripts.
-   **Footprint**: The entire interpreter is ~200KB. It fits anywhere.

---

## 2. The Antigravity Lua Standard

### Tables: The Universal Structure

In Lua, there are no arrays, sets, or hashmaps. There are only **Tables**.
A table is an associative array that can be indexed by numbers (array-like) or strings (dict-like).

```lua
local robot = {
    name = "Unitree Go2",
    battery = 100,
    sensors = { "lidar", "camera", "imu" }
}

print(robot.name)        -- Dictionary access
print(robot.sensors[1])  -- Array access (1-based!)
```

### Metatables & OOP

Lua does not have classes. It has **Metatables**.
We can define behavior for operations (like `+`, `-`, `index`) on tables.

**Pattern: The Prototype**
```lua
local Robot = {}
Robot.__index = Robot

function Robot.new(name)
    local self = setmetatable({}, Robot)
    self.name = name
    return self
end

function Robot:speak()
    print("I am " .. self.name)
end

local r = Robot.new("R1")
r:speak()
```

### Coroutines (Cooperative Multitasking)

Lua coroutines allow us to pause and resume functions. This is critical for game logic (Unity/Roblox) and async operations in single-threaded environments (Nginx).

```lua
local co = coroutine.create(function()
    for i = 1, 5 do
        print("step " .. i)
        coroutine.yield()
    end
end)

coroutine.resume(co) -- step 1
coroutine.resume(co) -- step 2
```

---

## 3. Global Context: Lua Evolution

*(Ingested from Wikipedia Research)*

### History & Philosophy (Brazil 1993)
Lua was created in 1993 by **Roberto Ierusalimschy**, **Luiz Henrique de Figueiredo**, and **Waldemar Celes** at the **Tecgraf** group of **PUC-Rio** in Brazil.

**Context**: Brazil had strict trade barriers on computer hardware and software. They couldn't import specialized software, so they built their own configurable language.
**Philosophy**: "Mechanisms, not policies." Lua provides the meta-mechanisms to build features, rather than built-in features.

### LuaJIT: The Speed Demon
**Mike Pall** created LuaJIT, a Just-In-Time compiler for Lua 5.1. It is famously fast, often approaching C speeds for numeric code. This version is what powers Neovim and OpenResty.

### Embeddability
Lua is designed to be embedded in a host C program.
C calls Lua, Lua calls C. The stack is shared. This makes it perfect for game engines (World of Warcraft, Roblox) and servers (Redis, Nginx).

---

## 4. Fleet Integration Patterns

### Neovim Configuration (`init.lua`)

We configure our editors using Lua to integrate with LSP servers (Language Server Protocol).

```lua
-- init.lua
local lspconfig = require('lspconfig')

lspconfig.pyright.setup {
    settings = {
        python = {
            analysis = {
                typeCheckingMode = "strict"
            }
        }
    }
}
```

### Redis Scripting (Atomic Logic)

When we need to check a value and decrement it atomically (e.g., rate limiting), we run Lua inside Redis.

```lua
-- rate_limit.lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = tonumber(redis.call('get', key) or "0")

if current + 1 > limit then
    return 0
else
    redis.call('incr', key)
    return 1
end
```

### Nginx/OpenResty

We use Lua to handle dynamic routing, authentication, and logging directly inside the Nginx worker process, avoiding the overhead of an upstream proxy.

---

## 5. Advanced Patterns

### FFI (Foreign Function Interface)

LuaJIT allows calling C functions directly without writing a C wrapper.

```lua
local ffi = require("ffi")
ffi.cdef[[
    int printf(const char *fmt, ...);
]]
ffi.C.printf("Hello %s\n", "World")
```

### Sandboxing (`setfenv`/`_ENV`)

We can execute untrusted user scripts by removing dangerous functions (`os.execute`, `io.open`) from their environment.

```lua
local env = { print = print, math = math }
local func = load("print(math.pi)", "user_script", "t", env)
func()
```

### Iterators & Closures

Lua relies heavily on closures (functions capturing their environment) for iteration.

```lua
function values(t)
    local i = 0
    return function()
        i = i + 1
        return t[i]
    end
end
```

---

## 6. Security Best Practices

1.  **Global Namespace Pollution**: Always use `local`.
2.  **Input Sanitation**: Never construct Lua code strings from user input (`loadstring`).
3.  **Resource Limits**: When sandboxing, use debug hooks to limit instruction count (prevent infinite loops).

---

## 7. Reference Material

-   [Programming in Lua (PiL)](https://www.lua.org/pil/)
-   [LuaJIT Documentation](https://luajit.org/)
-   [Neovim Lua Guide](https://github.com/nanotee/nvim-lua-guide)
-   [Redis Lua API](https://redis.io/commands/eval/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
