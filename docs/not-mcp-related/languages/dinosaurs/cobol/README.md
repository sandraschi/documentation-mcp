# COBOL: The Ledger

**Standard**: COBOL 2014 (Mandatory)
**Context**: "Business Oriented"
**Role**: Banking / Insurance / Government Backends
**Build System**: `gnucobol`
**Linting**: Strict Column Compliance

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for COBOL usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity COBOL Standard](#the-antigravity-cobol-standard)
    *   [Divisions (The Four Pillars)](#divisions-the-four-pillars)
    *   [PICTURE Clause (Decimal Precision)](#picture-clause-decimal-precision)
    *   [File Handling (ISAM)](#file-handling-isam)
3.  [Global Context: COBOL Evolution](#global-context-cobol-evolution)
    *   [History: Grace Hopper (1959)](#history-grace-hopper-1959)
    *   [The Y2K Crisis](#the-y2k-crisis)
    *   [Modern COBOL (OO & JSON)](#modern-cobol-oo--json)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Mainframe Integration (z/OS)](#mainframe-integration-zos)
    *   [Batch Processing (End of Day)](#batch-processing-end-of-day)
    *   [Data Migration](#data-migration)
5.  [Advanced Patterns](#advanced-patterns)
    *   [JSON GENERATE](#json-generate)
    *   [Object-Oriented COBOL](#object-oriented-cobol)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, COBOL is the **Foreign Language**. We do not run it, but we connect to systems that do.
When we integrate with a Viennese bank or a government agency API, at the bottom of the stack, there is COBOL.

**Why COBOL for SOTA 2026?**
-   **Precision**: Standard floating point (`float`, `double`) introduces rounding errors. COBOL's fixed-point decimal arithmetic is exact. This is non-negotiable for money.
-   **Readability**: Designed to be read by managers. `ADD TAX TO TOTAL GIVING NET.`
-   **Stability**: Code written in 1970 still compiles and runs today.

---

## 2. The Antigravity COBOL Standard

### Divisions (The Four Pillars)

Every program has exactly four divisions:
1.  **IDENTIFICATION DIVISION**: Metadata.
2.  **ENVIRONMENT DIVISION**: System configuration (File mapping).
3.  **DATA DIVISION**: Variable definitions (`WORKING-STORAGE`).
4.  **PROCEDURE DIVISION**: The code itself.

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.
       PROCEDURE DIVISION.
           DISPLAY 'Hello, World!'.
           STOP RUN.
```

### PICTURE Clause (Decimal Precision)

The magic of COBOL.
-   `9`: Numeric digit.
-   `V`: Implied decimal point.
-   `S`: Sign.

```cobol
       01  ACCOUNT-BALANCE     PIC S9(7)V99.  
       *   Holds: +/- 1234567.89
```

### File Handling (ISAM)

COBOL was built for processing files on tape/disk.
**ISAM (Indexed Sequential Access Method)** allows key-based lookup in flat files.

---

## 3. Global Context: COBOL Evolution

*(Ingested from Wikipedia Research)*

### History: Grace Hopper (1959)
Designed by the **Conference on Data Systems Languages (CODASYL)**, heavily influenced by **Grace Hopper**.
Goal: A machine-independent language for business.

### The Y2K Crisis
COBOL became infamous during Y2K because programmers originally used 2 digits for years (`PIC 99`) to save memory.
The fix involved expanding millions of lines of code to `PIC 9(4)`. THIS PROVED THE CODE WAS MAINTAINABLE.

### Modern COBOL (OO & JSON)
COBOL is not dead. The 2014 standard includes:
-   Object Orientation (Classes/Methods).
-   XML and JSON parsing/generation.
-   UTF-8 support.

---

## 4. Fleet Integration Patterns

### Mainframe Integration (z/OS)

We use IBM MQ or REST APIs (via z/OS Connect) to talk to mainframes.
We map our protobuf/JSON fields to COBOL `COPYBOOK` definitions.

### Batch Processing (End of Day)

COBOL excels at "End of Day" batch jobs. Read 10 million records, update balance, write 10 million records.
We orchestrate these jobs via Kubernetes CronJobs, but the core logic remains on big iron.

### Data Migration

When migrating legacy data to PostgreSQL, we must replicate COBOL's decimal rounding rules EXACTLY to avoid "penny errors".

---

## 5. Advanced Patterns

### JSON GENERATE

Modern compilers allow generating JSON directly from data structures.

```cobol
       JSON GENERATE JSON-TEXT FROM ACCOUNT-RECORD
```

### Object-Oriented COBOL

```cobol
       CLASS-ID. ACCOUNT INHERITS BASE.
       METHOD-ID. GET-BALANCE.
       ...
       END METHOD GET-BALANCE.
       END CLASS ACCOUNT.
```

---

## 6. Security Best Practices

1.  **Input Validation**: COBOL assumes fixed field lengths. Buffer overflows are impossible if `PIC` clauses are respected, but logic errors are common.
2.  **Authorization**: Rely on the host OS (RACF/TopSecret) for file access control.

---

## 7. Reference Material

-   [GnuCOBOL Manual](https://gnucobol.sourceforge.io/)
-   [IBM Enterprise COBOL Documentation](https://www.ibm.com/docs/en/cobol-zos)
-   [Open Mainframe Project](https://www.openmainframeproject.org/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
