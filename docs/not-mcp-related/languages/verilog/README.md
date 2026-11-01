# Verilog for FPGA Hardware: The SOTA 2026 Standard

**Standard**: SystemVerilog 2017 (Mandatory)
**Context**: "Parallelism at the Speed of Light"
**Role**: FPGA Logic / ASIC Design / Fast Signal Processing
**Toolchain**: Vivado / Verilator (Simulation)
**Linting**: `verilator --lint-only`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Verilog/SystemVerilog usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Verilog Standard](#the-antigravity-verilog-standard)
    *   [Always Blocks (`always_ff`, `always_comb`)](#always-blocks-always_ff-always_comb)
    *   [Interfaces](#interfaces)
    *   [State Machines (FSM)](#state-machines-fsm)
3.  [Global Context: HDL Evolution](#global-context-hdl-evolution)
    *   [Verilog vs VHDL](#verilog-vs-vhdl)
    *   [SystemVerilog: The Unification](#systemverilog-the-unification)
    *   [Simulation vs Synthesis](#simulation-vs-synthesis)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [LIDAR Pre-processing (FPGA)](#lidar-pre-processing-fpga)
    *   [Motor Control Loops](#motor-control-loops)
    *   [Verification (UVM Lite)](#verification-uvm-lite)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Clock Domain Crossing (CDC)](#clock-domain-crossing-cdc)
    *   [AXI4 Interconnect](#axi4-interconnect)
    *   [Pipelining](#pipelining)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Verilog describes the **Hardware**.
When milliseconds are too slow and microseconds are borderline, we go to nanoseconds.
We program Xilinx FPGAs to process raw sensor data *before* it hits the CPU.

**Why Verilog for SOTA 2026?**
-   **Hardware Acceleration**: Offload FFTs and Kalman Filters to dedicated logic gates.
-   **Determinism**: An FPGA has no OS jitter. The timing is cycle-perfect.
-   **Parallelism**: It doesn't have "threads". It has 100,000 lookup tables working simultaneously.

---

## 2. The Antigravity Verilog Standard

### Always Blocks (`always_ff`, `always_comb`)

We use SystemVerilog keywords to allow tools to check intent.
-   `always_ff`: Flip-flops (Clocked logic).
-   `always_comb`: Combinational logic (Gates).

```systemverilog
// Sequential Logic (Register)
always_ff @(posedge clk) begin
    if (reset)
        count <= 0;
    else
        count <= count + 1;
end

// Combinational Logic
always_comb begin
    is_max = (count == 8'hFF);
end
```

### Interfaces

Bundle signals together. Instead of passing `clk, reset, data_in, valid_in, ready_out`, pass an `interface`.

```systemverilog
interface sensor_bus(input logic clk);
    logic [31:0] data;
    logic valid;
    
    modport master (output data, valid);
    modport slave (input data, valid);
endinterface
```

### State Machines (FSM)

The bread and butter of control logic.
Use `enum` for states.

```systemverilog
typedef enum logic [1:0] {IDLE, READ, WRITE} state_t;
state_t current_state, next_state;

always_ff @(posedge clk) current_state <= next_state;

always_comb begin
    case (current_state)
        IDLE: next_state = start ? READ : IDLE;
        // ...
    endcase
end
```

---

## 3. Global Context: HDL Evolution

*(Ingested from Wikipedia Research)*

### Verilog vs VHDL
-   **Verilog**: C-like, terse. Used widely in Silicon Valley.
-   **VHDL**: Ada-like, verbose, strict typing. Used widely in Defense/Europe.
**Antigravity Choice**: SystemVerilog (Verilog superset) because it is the industry standard for verification and design.

### SystemVerilog: The Unification
Combined Verilog 2005 with verification features (Assertions, Classes). It allows "Design" and "Verification" to happen in the same language.

### Simulation vs Synthesis
-   **Simulation**: Running the code on a CPU to verify logic (Verilator).
-   **Synthesis**: Mapping the code to physical gates (LUTs/Flip-Flops) on the FPGA (Vivado).
*Note: Not all valid SystemVerilog is synthesizable.*

---

## 4. Fleet Integration Patterns

### LIDAR Pre-processing (FPGA)

The raw UDP stream from a Livox LIDAR is 200Mbps.
An FPGA parses the packets, filters noise, and converts polar to cartesian coordinates *wire-speed*, presenting a clean point cloud to the main PC via PCIe.

### Motor Control Loops

FOC (Field Oriented Control) requires updates at 20kHz-100kHz.
Implementing the PID loops in FPGA hardware guarantees perfectly stable control loops regardless of CPU load.

### Verification (UVM Lite)

We write testbenches in SystemVerilog.
We use `assert` statements to formally verify properties.
`assert property (@(posedge clk) req |-> ##[1:3] ack);` (If Request, then Ack within 1-3 cycles).

---

## 5. Advanced Patterns

### Clock Domain Crossing (CDC)

Passing signals between the 100MHz system clock and the 50MHz sensor clock.
**Rule**: Always use a 2-stage synchronizer or a FIFO. Never sample asynchronous signals directly.

### AXI4 Interconnect

The standard bus for connecting IP blocks. Understanding AXI-Stream (for data) and AXI-Lite (for control) is mandatory for integrating with the ARM processor (Zynq/Ultrascale+).

### Pipelining

Breaking a complex calculation `A * B + C` into stages separated by registers to increase maximum frequency (`Fmax`).

---

## 6. Security Best Practices

1.  **Bitstream Security**: Authenticate the bitstream to prevent hardware trojans.
2.  **Reset Logic**: Ensure every register has a known reset state. An X (unknown) state can lock up a state machine forever.

---

## 7. Reference Material

-   [IEEE 1800-2017 SystemVerilog Standard](https://standards.ieee.org/standard/1800-2017.html)
-   [ZipCPU (FPGA Design Blog)](https://zipcpu.com/)
-   [ASIC World](https://www.asic-world.com/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
