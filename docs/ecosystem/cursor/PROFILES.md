# Cursor Public Profiles

**Status:** Active (platform feature)  
**Updated:** 2026-06-06  
**Help:** [cursor.com/help/account-and-billing/profiles](https://cursor.com/help/account-and-billing/profiles)  
**Claim handle:** [cursor.com/profile](https://cursor.com/profile)

Public Profiles are **shareable identity pages** at `cursor.com/@yourhandle`. Despite living under Account and billing in Cursor Help, they are **not** billing profiles, seat switching, or multi-account management.

---

## What it is

| Item | Detail |
|------|--------|
| **URL** | `cursor.com/@yourhandle` after you claim a handle |
| **Content** | Name, avatar, join date, up to 4 external links, usage activity over time |
| **Setup** | Sign in at [cursor.com/profile](https://cursor.com/profile), claim handle, add links |
| **Visibility** | Public by default when handle is claimed; toggle to private |

Name and avatar come from Cursor account settings. Edits appear on the live profile on next load.

---

## What it is not

| Misread | Reality |
|---------|---------|
| Multiple billing profiles | One subscription per Cursor account |
| Work vs personal account switcher | No in-app profile switcher |
| Team seat / org management | Teams/Enterprise dashboard |
| Cloud Agent spend controls | Dashboard → Cloud Agents / billing limits |

### Separate personal + work accounts

Cursor still has no native multi-account switch. Workaround: separate installs or launch with distinct user data dir:

```powershell
cursor --user-data-dir="D:\CursorProfiles\work"
```

Each dir keeps its own login, settings, MCP config, and billing.

---

## Privacy

| Setting | Who can view |
|---------|----------------|
| **Public** (default on claim) | Anyone with the link, including logged-out visitors |
| **Private** | Only you, signed in as owner |

Usage charts on the profile reflect your Cursor activity over time and update as you use the product. Keep **private** if you do not want activity visible even in aggregate form.

---

## Constraints

- Handle is **permanent** after claim — choose carefully
- Up to **four links** (GitHub, X, LinkedIn, personal site, etc.)
- Delete Cursor account → profile and handle removed

---

## Fleet stance

Optional. No operational impact on MCP fleet, Cloud Agents, or billing guardrails. Use only if you want a public Cursor identity link; otherwise skip or stay private.

---

## References

- [Profiles help](https://cursor.com/help/account-and-billing/profiles)
- [Billing and payments](https://cursor.com/help/account-and-billing/billing)
- [Cloud Agents (fleet guide)](CLOUD_AGENTS.md)
