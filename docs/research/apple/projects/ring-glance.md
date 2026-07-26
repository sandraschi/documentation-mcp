# Ring Glance

**Model:** One-time $3.99–6.99  
**Comps:** Ring app (bloated); you want **doorbell + 2 cams, fast**

## Product

Login to Ring account (official API patterns from fleet ring-mcp research). Show live view for doorbell and selected cameras. Widget: last snapshot. Optional critical alerts for doorbell press.

## Fleet reuse

| Piece | Source |
|-------|--------|
| Graph / WebRTC patterns | [ring-mcp](../../integrations/ring-mcp.md), ring-mcp webapp |
| Integration docs | projects/ring-mcp in fleet |

## Monetization

Paid app — single SKU. Ring users already pay for hardware/sub; they’ll pay a few bucks for a cleaner client if reviews are good.

## AI angle

- Optional: on-device Vision summary “package detected” on snapshot — careful with battery and review (must work for real)

## Effort / revenue

- **Effort:** Low–medium if ring-mcp auth/stream logic ports cleanly
- **Upside:** Spiky sales when Ring app frustrates users; maintain when API changes

## Risks

- Unofficial API — can break; disclose in release notes; budget maintenance time
