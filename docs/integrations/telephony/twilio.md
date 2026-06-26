# Twilio Integration & Austrian Regulatory Compliance (2026)

This document outlines the standard operating procedures for integrating **Twilio** into the RoboFang/MCP fleet, specifically focusing on the high-fidelity regulatory requirements for **Austrian (Vienna)** operations.

## 1. Overview
Twilio serves as the primary telephony bridge for **Autonomous Emergency Dispatch (AED)** and critical SMS alerting. Due to EU anti-spoofing regulations and Austrian RTR mandates, provisioning a number in Vienna (+43 1) requires significant upfront documentation.

## 2. Austrian Regulatory Bundle (+43)
To purchase an Austrian phone number, you must submit a **Regulatory Bundle** through the Twilio Console.

### Required Documentation
| Entity Type | Required Proof of Identity | Required Proof of Address |
| :--- | :--- | :--- |
| **Individual** | Passport or Government ID | Utility Bill, Rent Receipt, or Tax Assessment |
| **Business** | Commercial Register Excerpt (*Firmenbuch*) | Official Proof of Business Address |

> [!IMPORTANT]
> **Address Locality Requirement**: To obtain a prefix for a specific city (e.g., **01** for Vienna), your proof of address MUST be within that city's geographic boundary. International addresses are not accepted for Austrian local numbers.

### Step-by-Step Procedure:
1. Log in to the [Twilio Console](https://www.twilio.com/console).
2. Navigate to **Phone Numbers > Regulatory Compliance > Bundles**.
3. Create a new "Austria" bundle.
4. Upload high-resolution scans of your documentation.
5. Wait **3–5 business days** for Twilio's regulatory team to verify.
6. Once "Approved," you can assign the bundle to a new +43 number.

## 3. SOTA 2026 Pricing (Austria)
*As of April 2026, prices are estimated in USD.*

### Fixed Costs (Monthly)
- **Local Number (+43 1)**: ~$1.00 / month
- **Mobile Number (+43 6XX)**: ~$6.00 / month
- **Toll-Free (+43 800)**: ~$25.00 / month

### Usage Costs (Pay-as-you-go)
- **Outgoing Voice (Local)**: ~$0.015 / minute
- **Outgoing Voice (Mobile)**: ~$0.08 - $0.20 / minute (depending on carrier)
- **Outgoing SMS**: ~$0.07 / segment
- **Incoming SMS**: Free (typically)

## 4. Anti-Spoofing & STIR/SHAKEN
Austria uses strict caller ID verification logic. To ensure your emergency calls are not blocked by A1, Magenta, or Drei:
- **Verified Caller ID**: You MUST use the Austrian number purchased through Twilio as your `FROM` number.
- **No Spoofing**: Never attempt to spoof a number you do not own.
- **Truthful TTS**: Always identify the system as an AI (Autonomes Notfall-System) to build trust with dispatchers.

## 5. Emergency Dispatch Best Practices
When using the `telephony-mcp` for 122/133/144 dispatch:
1. **German First**: Always use `de-AT` TTS.
2. **Standard Templates**: Use the codified scripts in `robofang/docs/ROBOT_SAFETY.md`.
3. **Loop-Back**: Always provide a "Callback" number (your Twilio number) so dispatchers can call back to confirm.

---
**Status**: Industrial / Beta
**Contact**: [sandraschi](https://www.moltbook.com/sandraschi)
**Last Updated**: 2026-04-19
