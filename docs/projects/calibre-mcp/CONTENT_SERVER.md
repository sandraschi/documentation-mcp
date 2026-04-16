# Calibre Content server, calibredb, and direct `metadata.db`

**Companion to** [README.md](./README.md). Architecture note for **fleet / integration** decisions.

---

## Summary

Calibre’s **calibredb** CLI can target a running **Content server** using a library URL such as `http://host:port/#library_id` (see [calibredb — library path](https://manual.calibre-ebook.com/generated/en/calibredb.html)). That path is **official**, but it is **not** remote direct access to the **`metadata.db`** file. For CalibreMCP, **local SQLAlchemy access to `metadata.db`** remains the high-value approach; a parallel “remote CLI” mode has **limited upside** relative to the maintenance cost.

---

## What “remote” via CLI actually is

- **Not:** Opening `metadata.db` over the network or mounting the library folder remotely.
- **Instead:** Calibre’s **Content server** exposes a **supported** remote protocol that **calibredb** (and Calibre’s libraries) use to perform **allowed** operations over HTTP, with **timeouts**, **auth** (username/password, HTTPS in production), and **whatever subset** the server implements.

So “remote calibredb” means **remote Calibre server semantics**, not **full local-database semantics**.

---

## Why direct `metadata.db` manipulation wins for this MCP

| Concern | Local `metadata.db` (CalibreMCP’s primary design) | Content server + calibredb remote |
|--------|-----------------------------------------------------|-------------------------------------|
| **Metadata depth** | Full SQLAlchemy models, joins, counts, analytics | Whatever the remote API / calibredb exposes over that link |
| **RAG / LanceDB** | Natural fit: index from DB + files on disk | No local DB file; reindexing / embeddings need another story |
| **Performance** | Single-machine SQLite (WAL), batch queries | Network latency, server limits, timeouts (default e.g. 2 minutes in docs context) |
| **Consistency** | Same process as file paths and covers | Auth, TLS, proxy, **URL prefix** (`--url-prefix`) complicate every call |
| **Stability** | Schema is your ORM + migrations discipline | Server version skew; fewer guarantees than “we own the DB file” |

---

## Limited upside of duplicating workflows for “remote CLI only”

Implementing a **second** backend that only shells **calibredb** against `http://…/#…` would:

- **Not** replicate CalibreMCP’s **direct-DB** features (rich stats, custom queries, local RAG pipeline) without a **separate** design.
- **Still** require **credentials management**, **HTTPS**, and **error** handling for network failure—similar to any HTTP client.
- **Overlap** partially with what users already get by running CalibreMCP **on the machine that holds the library** (or over **SMB/NFS** to the folder, if policy allows)—still file-backed `metadata.db`.

So the **incremental value** of remote-only CLI integration is **narrow**: mainly **“agent on laptop, library only on a home server with Content server, no file share”** scenarios, with **reduced** tool surface and **no** parity with local DB tools.

---

## When a Content server still matters

- **Human reading / OPDS / browser**: Calibre’s Content server is the right product ([server manual](https://manual.calibre-ebook.com/server.html)).
- **Automation without CalibreMCP on the host**: **calibredb** against the Content server URL is the **supported** automation channel from another machine—**if** the operations you need are supported remotely.

---

## Recommendation for the codebase

- **Keep** first-class support for **local library path → `metadata.db`** as the **full-featured** mode.
- If remote access is needed later, treat it as an **explicit degraded mode**: document **capability gaps**, **no** promise of RAG/SQL parity, and prefer **one** thin adapter (calibredb or a small HTTP wrapper) rather than pretending it equals direct DB access.

---

## References

- [The calibre Content server](https://manual.calibre-ebook.com/server.html) — auth, HTTPS, reverse proxy, `calibre-server`, URL prefix.
- [calibredb — `--with-library` / Content server URL](https://manual.calibre-ebook.com/generated/en/calibredb.html) — `http://hostname:port/#library_id`, library id `-` for listing.

---

[← Back to project README](./README.md)
