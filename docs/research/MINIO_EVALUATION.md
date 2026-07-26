# MinIO Evaluation

**Date:** 2026-06-25  
**Status:** Borderline — useful but licensing changed  
**Source:** https://github.com/minio/minio (archived)  
**License:** AGPLv3 (open-source)/ Commercial (AIStor)  

---

## 1. What it is

**S3-compatible object storage** in a single Go binary. Any code that can speak HTTP can PUT/GET files — no special SDK required. Think "S3 running on your own machine."

**What it solves for the fleet:** A shared file store any MCP server can upload/download from. Screenshots, exports (STL, DXF, CSV), file exchange between servers (qcad → freecad → godot pipeline), artifact storage for build outputs.

---

## 2. License — CRITICAL UPDATE

| Aspect | Detail |
|---|---|
| **Open-source repo** | **Archived** (April 2026). No more open-source releases. |
| **OS license** | AGPLv3 — strict copyleft. Running it as a network service requires distributing your source to any user who interacts with it. |
| **Current product** | **MinIO AIStor** — commercial replacement. Has a Free tier (single-node, community) and paid Enterprise tiers. |
| **For fleet use** | AGPLv3 infrastructure use (not modifying MinIO itself) is legally debated. The safer path is AIStor Free via Docker. |

**Bottom line:** MinIO is no longer a pure open-source project. AIStor Free covers the use case but adds vendor dependency.

---

## 3. Stars & activity (pre-archive)

61k stars, 1B+ Docker pulls, 521 releases. The archived repo is read-only — ongoing development is in AIStor.

---

## 4. Fleet fit

| Use case | Works? | How |
|---|---|---|
| Screenshot artifact store | Yes | PUT `screenshot-001.png` from webapp, GET from dashboard |
| File exchange between MCP servers | Yes | qcad exports DXF → MinIO → freecad reads DXF |
| Build output storage | Yes | NSIS installers, mcpb bundles, exported CSV |
| Shared dataset storage | Yes | CFD results, training data, media files |

### Concrete deployment

```yaml
services:
  minio:
    image: minio/minio:latest
    ports:
      - "11070:9000"      # S3 API
      - "11071:9001"      # Console UI
    env:
      MINIO_ROOT_USER: fleet
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    volumes:
      - minio_data:/data
    command: server /data --console-address :9001
```

Usage from any MCP server (no SDK needed):

```python
import httpx
r = httpx.put("http://localhost:11070/fleet-bucket/screenshot.png",
    content=image_bytes,
    headers={"Authorization": f"Bearer {token}"})
```

---

## 5. Key features

- **S3-compatible API** — any S3 SDK or tool (boto3, mc, rclone) works
- **Web UI Console** (port 9001) — browse, upload, manage buckets
- **Presigned URLs** — time-limited download links (e.g., for Godot to fetch a GLB)
- **Versioning** — per-bucket object versioning with history
- **Notifications** — bucket events → webhooks, Kafka, etc.
- **Encryption** — SSE-S3, SSE-C, TLS in transit
- **IAM policies** — per-bucket, per-user access control

---

## 6. Resource requirements

- **Binary:** ~50 MB (Go, static)
- **RAM:** ~100 MB idle, scales with concurrent operations
- **Disk:** Arbitrary (mapped volume)
- **Docker:** Single compose service, minimal overhead

---

## 7. Limitations

- **Archived repo** — no more open-source contributions; future is commercial AIStor
- **AGPLv3** — legally contentious for infrastructure use in mixed environments
- **Not a filesystem** — no POSIX semantics, no FUSE without extra tools
- **Performance ceiling on Windows** — optimized for Linux, NTFS adds overhead
- **Case sensitivity** — S3 bucket names are lowercase-only
- **NTFS path length** — object keys with deep prefixes can hit MAX_PATH

---

## 8. Alternative (lighter weight)

If all you need is a shared file store without S3 compatibility or a web UI, consider `fileops` tools or a simple HTTP file server (Python's `http.server` or Caddy's `file_server`). MinIO only pays off if you need the S3 API surface (presigned URLs, versioning, notifications, multi-bucket policies) or the web console.

---

## 9. Verdict

**Weak yes if you need S3 features; skip if simple file storage suffices.** The archived repo and AGPLv3 are real concerns. For the fleet's current file exchange needs (cross-server artifacts, screenshots), a simpler solution (Caddy file_server or even a shared network directory) covers 80% of the use case with zero license baggage. Revisit if the fleet grows to need S3 API features at scale.
