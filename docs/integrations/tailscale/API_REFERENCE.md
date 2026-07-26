# Tailscale API Reference (Fleet Notes)

**Refreshed:** 2026-06-20, against `tailscale-mcp` `src/tailscalemcp/client/api_client.py` directly — every endpoint below is a real method on `TailscaleAPIClient`, not a guess at what the Tailscale Admin API might offer.

This page covers the REST endpoints this server actually calls. **Funnel and Taildrop are not REST calls** — they shell out to the `tailscale` CLI binary instead (see [FEATURES.md](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/FEATURES.md) and the architecture note at the bottom of this page). The previous version of this page invented REST endpoints for both that don't exist anywhere in Tailscale's actual API.

---

## Authentication

Every request carries a bearer token:

```
Authorization: Bearer tskey-api-...
```

Base URL is built per-tailnet at client init: `https://api.tailscale.com/api/v2/tailnet/{tailnet}`. All the endpoints below are relative to that base.

## Devices

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/devices` | `list_devices()` |
| GET | `/devices/{device_id}` | `get_device(device_id)` |
| POST | `/devices/{device_id}` | `update_device(device_id, updates)` |
| DELETE | `/devices/{device_id}` | `delete_device(device_id)` |

`update_device` is the one real write endpoint for devices — rename, tag, and authorize are all expressed as different `updates` payloads to this same endpoint, not separate REST calls.

## ACL Policy

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/acl` | `get_acl_policy()` |
| POST | `/acl` | `update_acl_policy(policy)` |

## DNS

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/dns/nameservers` | `get_dns_config()` |
| POST | `/dns/nameservers` | `update_dns_config(config)` |

## Services (beta — subject to change upstream)

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/services` | `list_services()` |
| GET | `/services/{id}` | `get_service(id)` |
| POST | `/services` | `create_service(payload)` |
| POST | `/services/{id}` | `update_service(id, payload)` |
| DELETE | `/services/{id}` | `delete_service(id)` |

Responses are parsed into a `Service` model (`src/tailscalemcp/models/service.py`), not raw dicts.

## Users

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/users?type=&role=` | `list_users(user_type, role)` |
| GET | `/users/{id}` | `get_user(id)` |

## Device invites

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/devices/{device_id}/device-invites` | `list_device_invites(device_id)` |
| POST | `/devices/{device_id}/device-invites` | `create_device_invites(device_id, invites)` |
| GET | `/device-invites/{id}` | `get_device_invite(id)` |
| DELETE | `/device-invites/{id}` | `delete_device_invite(id)` |
| POST | `/device-invites/{id}/resend` | `resend_device_invite(id)` |
| POST | `/device-invites/-/accept` | `accept_device_invite(invite)` |

## User invites

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/tailnet/{t}/user-invites` | `list_user_invites(tailnet)` |
| POST | `/tailnet/{t}/user-invites` | `create_user_invites(invites, tailnet)` |
| GET | `/user-invites/{id}` | `get_user_invite(id)` |
| DELETE | `/user-invites/{id}` | `delete_user_invite(id)` |
| POST | `/user-invites/{id}/resend` | `resend_user_invite(id)` |

No `accept` endpoint for user invites — that distinction (device invites *can* be self-accepted via API, user invites can't) is real and worth remembering; it's not an oversight in this client.

## Device posture attributes

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/devices/{device_id}/attributes` | `get_device_posture_attributes(device_id)` |
| POST | `/devices/{device_id}/attributes/{key}` | `set_custom_device_posture_attribute(...)` |
| DELETE | `/devices/{device_id}/attributes/{key}` | `delete_custom_device_posture_attribute(...)` |
| PATCH | `/tailnet/{t}/device-attributes` | `batch_update_device_posture_attributes(nodes, comment, tailnet)` |

## Device keys

| Method | Endpoint | Client method |
|---|---|---|
| POST | `/devices/{device_id}/expire` | `expire_device_key(device_id)` |
| POST | `/devices/{device_id}/key` | `update_device_key(device_id, key_expiry_disabled)` |
| POST | `/devices/{device_id}/ip` | `set_device_ip(device_id, ipv4)` |

## Logging

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/tailnet/{t}/logging/configuration` | `list_configuration_audit_logs(...)` |
| GET | `/tailnet/{t}/logging/network` | `list_network_flow_logs(...)` |
| GET | `/tailnet/{t}/logging/{log_type}/stream/status` | `get_log_streaming_status(log_type, tailnet)` |
| GET | `/tailnet/{t}/logging/{log_type}/stream` | `get_log_streaming_configuration(log_type, tailnet)` |
| PUT | `/tailnet/{t}/logging/{log_type}/stream` | `set_log_streaming_configuration(log_type, config, tailnet)` |

## Webhooks

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/tailnet/{t}/webhooks` | `list_webhooks(tailnet)` |
| POST | `/tailnet/{t}/webhooks` | `create_webhook(endpoint_url, provider_type, ...)` |
| GET | `/tailnet/{t}/webhooks/{id}` | `get_webhook(id, tailnet)` |
| PATCH | `/tailnet/{t}/webhooks/{id}` | `update_webhook(id, updates, tailnet)` |
| DELETE | `/tailnet/{t}/webhooks/{id}` | `delete_webhook(id, tailnet)` |
| POST | `/tailnet/{t}/webhooks/{id}/rotate` | `rotate_webhook_secret(id, tailnet)` |

## Tailnet settings & contacts

| Method | Endpoint | Client method |
|---|---|---|
| GET | `/tailnet/{t}/tailnet-settings` | `get_tailnet_settings(tailnet)` |
| PATCH | `/tailnet/{t}/tailnet-settings` | `update_tailnet_settings(settings, tailnet)` |
| GET | `/tailnet/{t}/contacts` | `get_contact_preferences(tailnet)` |
| PUT | `/tailnet/{t}/contacts` | `update_contact_preferences(contacts, tailnet)` |

## Error responses

Real exception hierarchy from `src/tailscalemcp/exceptions.py` — not a generic dict-based error scheme:

| HTTP status | Exception raised |
|---|---|
| 401 | `AuthenticationError` |
| 404 | `NotFoundError` |
| 429 | `RateLimitExceededError` |
| other 4xx/5xx | `TailscaleAPIError` |

All inherit from `TailscaleMCPError`, which carries `message`, `code`, and a `details` dict (`.to_dict()` for the wire shape). 401s specifically get extra handling at the tool layer — see [TRAPS_AND_PITFALLS.md §6](../../standards/TRAPS_AND_PITFALLS.md#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error).

## Rate limiting and retry — real defaults, not invented numbers

From `src/tailscalemcp/config.py` and `client/rate_limiter.py` / `client/retry.py`:

- **Rate limit**: 1 request/second by default (`rate_limit_per_second`), token-bucket style over a 60-second window — configurable, but this is what ships.
- **Retries**: 3 attempts by default, exponential backoff (`backoff_factor=2.0`) with up to 25% random jitter, capped at 60 seconds total wait.
- **Retried on**: network errors, HTTP 429/500/502/503/504, timeouts. **Not retried**: 401/404/429-as-final (rate limit itself raises `RateLimitExceededError` rather than silently retrying forever — the retry-on-429 case is for upstream Tailscale 429s during the request, separate from this client's own self-imposed 1/sec limiter).
- **Connection pooling**: `max_connections=10`, `max_keepalive_connections=5` by default.

These aren't aspirational — they're the literal `Field(default=...)` values in `TailscaleConfig`. Override via `.env` if a workload needs different limits.

## What's not REST: Funnel and Taildrop

Both `manage_funnel` and `manage_taildrop` operations shell out to the **`tailscale` CLI binary** (`src/tailscalemcp/utils/tailscale_cli.py`'s `TailscaleCLI` wrapper) rather than calling a REST endpoint — there is no `/api/v2/.../funnel` or `/api/v2/.../files` endpoint in Tailscale's actual API, despite what older drafts of fleet documentation claimed. `FunnelManager` and `TaildropManager` both check CLI availability at init (`use_cli`) and degrade gracefully: Funnel raises a clear error if the CLI isn't found, while Taildrop falls back to a **simulated transfer** (progress percentages, no actual file movement) if the CLI is unavailable — worth knowing if a Taildrop test "succeeds" but no file actually arrives anywhere.
