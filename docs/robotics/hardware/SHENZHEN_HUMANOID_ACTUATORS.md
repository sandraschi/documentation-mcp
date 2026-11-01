---
title: "Shenzhen humanoid actuators — die halbe Miete"
category: reference
status: active
audience: mcp-dev
last_updated: 2026-07-21
related:
  - not-mcp-related/general-ai/regions/prc-dual-vectors-openweights-and-goes.md
  - robotics/README.md
---

# Shenzhen humanoid actuators

**The humdinger of 2026 industrial policy:** 100+ Shenzhen startups shipping humanoids *and* humanoid parts. The scarce piece is not the aluminum frame or the Pi-class brain — it is the **joint module**.

## Die halbe Miete

High-torque **mini motors with integrated reduction gear** (often strain-wave / harmonic) plus encoder and **force / torque feedback** in one can. Buy those, and you can hammer the rest together in a warehouse: structure, wiring, compute, FOSS stack.

Without them, you are reinventing Harmonic Drive + frameless torque motor + dual encoder + driver — at Western cobot BOM prices that make a 30–40 DoF humanoid dead on arrival.

**Where to buy them:** Shenzhen (and the broader PRD supplier mesh). Samples in weeks; bulk in a month-ish from the better shops. Western catalogs exist; volume and iteration speed do not.

## What “integrated joint” usually means

| Layer | Typical contents |
| --- | --- |
| Gear | Harmonic (strain-wave) for arms / precision; planetary often for legs / impact |
| Motor | Frameless or compact BLDC / torque motor |
| Sense | Single or dual encoder; some modules expose torque / current as force proxy |
| Drive | Onboard driver; CANopen / EtherCAT / RS485 common |
| Mech | Hollow shaft options for cable routing through the joint |

Example supplier class (illustrative, not an endorsement list): ZHR Motor (Shenzhen), Picea Motion, Makon-class integrated actuators, plus dozens of harmonic-drive specialists feeding the humanoid wave. Trade shows (e.g. ITES China humanoid zones) are where the full chain sits in one hall.

## Fleet read

- Same PRC pattern as GOES / batteries / FOSS models: **scale the hard mid-tech component**, let warehouses worldwide assemble the rest.
- Embodied fleet plans (Bumi, Unitree, Yahboom, Resonite twins) should assume **actuator sourcing geography** the way they assume GPU geography.
- Pair with open-weight edge brains ([Jackrong](../../models/JACKRONG_DISTILL_FACTORY.md), Gemma/Qwen local) and you get a path to capable robots that is not gated on Boston Dynamics prices — gated on **who sells the joints**.

Broader dual-vector note: [prc-dual-vectors-openweights-and-goes.md](../../not-mcp-related/general-ai/regions/prc-dual-vectors-openweights-and-goes.md).

Canonical robotics TSOT for doctrine/ops: [robotics-mcp](file:///D:/Dev/repos/robotics-mcp/README.md).
