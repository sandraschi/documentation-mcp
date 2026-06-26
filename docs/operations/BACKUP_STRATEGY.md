# Goliath Backup Strategy

**Status:** Active  
**Last updated:** 2026-05-01  
**Owner:** Sandra

---

## Philosophy

Goliath has 30TB of storage across spinners. Not all data is equal. The strategy
is tiered by replaceability and irreplaceability — expensive cloud backup for the
small pile of things that cannot be recovered, cheap physical offsite for the large
pile of things that can be recovered but would be annoying to.

Current connectivity: 300/50 Mbps (Magenta). Pending upgrade to Wien Energie
SuperSchnell 1000 (1/1 Gbps symmetric) — this unlocks practical cloud seeding
and makes nightly rclone jobs fast enough to not matter.

---

## Data Inventory & Tier Assignment

| Data | Est. Volume | Replaceable? | Tier |
|---|---|---|---|
| GitHub repos (fleet MCP servers) | ~10 GB | Yes — GitHub | GitHub (free) |
| mcp-central-docs (mcd) | ~500 MB | No — years of standards/docs | B2 cloud |
| Calibre library (13k books) | ~500 GB | Partially — Anna's Archive for most | B2 cloud |
| Rare/hard-to-find anime archive | ~1 TB | No | B2 cloud |
| Active dev projects (non-git) | ~100 GB | No | B2 cloud |
| Goliath config / dotfiles / secrets | ~50 GB | No | B2 cloud |
| Plex mainstream content | ~18 TB | Yes — re-downloadable | Steve (physical) |
| Running anime/TV series (ongoing) | ~few GB/mo delta | Mostly yes | Steve (physical) |
| Ollama models / LM Studio models | ~200 GB | Yes — re-downloadable | No backup needed |
| Windows OS / installed software | varies | Yes — reinstallable | No backup needed |

**Cloud backup total: ~2 TB**  
**Physical offsite total: ~18–20 TB**

---

## Tier 1: Cloud Backup (B2 + rclone)

### Provider: Backblaze B2

- S3-compatible object storage
- $6.95/TB/month storage
- Free egress up to 3x monthly average (effectively free for backup-and-rarely-restore)
- At ~2TB: **~$14/month (~€13)**
- No per-file fees at this scale

### Tool: rclone

rclone is the standard tool for this. Encrypts client-side before upload
(so Backblaze never sees plaintext), S3-compatible, scriptable, runs on Windows.

**rclone config pattern:**

```
# Create B2 remote
rclone config
# -> New remote -> name: b2-goliath -> type: b2
# -> account: <B2_KEY_ID> -> key: <B2_APP_KEY>

# Create encrypted remote on top of B2
rclone config
# -> New remote -> name: b2-crypt -> type: crypt
# -> remote: b2-goliath:goliath-backup
# -> filename_encryption: standard
# -> directory_name_encryption: true
# -> password: <strong passphrase — store in KeePass>
```

**Backup job (PowerShell, runs via Task Scheduler nightly):**

```powershell
# D:\Dev\repos\mcp-central-docs\scripts\backup-cloud.ps1
$rclone = "C:\tools\rclone\rclone.exe"

$jobs = @(
    @{ src = "D:\Dev\repos\mcp-central-docs"; dst = "b2-crypt:mcd" },
    @{ src = "D:\Calibre Library";            dst = "b2-crypt:calibre" },
    @{ src = "D:\Anime\rare";                 dst = "b2-crypt:anime-rare" },
    @{ src = "D:\Dev\repos";                  dst = "b2-crypt:dev-repos" },
    @{ src = "C:\Users\sandr\AppData\Roaming\Claude"; dst = "b2-crypt:claude-config" }
)

foreach ($job in $jobs) {
    & $rclone sync $job.src $job.dst `
        --transfers 8 `
        --checkers 16 `
        --fast-list `
        --log-file "D:\Dev\repos\temp\rclone-backup.log" `
        --log-level INFO
}
```

**Run schedule:** Nightly at 03:00 via Windows Task Scheduler.
Set to run only when machine is idle and on AC power (always true for Goliath).

**Initial seed time estimate (at 1 Gbps upload):**
- 2TB at 800 Mbps effective: ~5–6 hours
- Run once, manually, then let nightly delta jobs take over

### What to back up to B2 — checklist

- [x] `D:\Dev\repos\mcp-central-docs\` — the entire mcd
- [x] `D:\Calibre Library\` — all books
- [x] Active dev projects not in git
- [x] Claude Desktop config (`%APPDATA%\Claude\`)
- [x] Claude MCP config (`claude_desktop_config.json`)
- [x] Cursor / Windsurf / OpenCode configs
- [x] KeePass database (already encrypted at rest)
- [x] Rare/irreplaceable anime that is genuinely hard to re-find
- [ ] Identify any other irreplaceable data not listed above

### What NOT to back up to B2

- Plex mainstream content → Steve
- Ollama / LM Studio models → re-downloadable
- Windows OS / installed apps → reinstallable
- node_modules, venvs, __pycache__ → always exclude these

**rclone excludes to always add:**

```
--exclude "node_modules/**"
--exclude ".venv/**"
--exclude "**/__pycache__/**"
--exclude "*.pyc"
--exclude ".git/**"
```

---

## Tier 2: Physical Offsite (Steve)

### What

The full Plex media library (~18–20 TB) lives on spinners in Goliath.
A copy lives at Steve's place in Vienna on an equivalent set of drives.

Steve is retired bank IT. He understands what the drive is for and
that it should not be unplugged, reformatted, or otherwise interfered with.
The drives are fire insurance, not an active sync target.

### Current state

Drives at Steve's are a periodic manual sync — when there's a significant
addition (new season, large haul) Sandra physically brings a drive or
uses the local network if Steve is on the same LAN during a visit.

### Improvement with 1 Gbps uplink (pending Wien Energie upgrade)

Once symmetric gigabit is available, an automated nightly rclone sync
to Steve's NAS/machine over Tailscale becomes viable for the delta only
(few GB/month of new anime/TV series). The initial 20TB state is already
there physically. Only new content needs to travel.

**Tailscale-based rclone sync pattern (future):**

```powershell
# Requires: Tailscale on both Goliath and Steve's machine
# Requires: rclone on Steve's machine or SFTP/SMB share exposed via Tailscale

& $rclone sync "D:\Plex Media\" "sftp:steve-goliath:/media/plex/" `
    --transfers 4 `
    --bwlimit 50M `   # be polite to Steve's connection
    --log-file "D:\Dev\repos\temp\rclone-steve.log"
```

### Steve's hardware requirements

Steve needs enough attached storage to hold the media library.
Current ~18TB → at least 2x 10TB or 1x 20TB spinner.
Drives should be checked for health annually (CrystalDiskInfo).

---

## Local 3-2-1 (existing, not changing)

Goliath already runs local 3-2-1 to internal spinners.
This is not documented here in detail — it handles the fast-restore case
(accidental deletion, drive failure) which cloud and offsite do not serve well.

The three tiers together:

| Tier | Protects against | Location |
|---|---|---|
| Local spinners (3-2-1) | Drive failure, accidental deletion | Goliath |
| B2 cloud (rclone encrypted) | Fire, theft, catastrophic hardware loss | Backblaze US |
| Steve's drives | Fire, theft (for media bulk) | Vienna (Steve) |

---

## Cost Summary

| Item | Monthly cost |
|---|---|
| Backblaze B2 (~2TB) | ~€13 |
| Steve's drives (amortised, one-time ~€300) | ~€3 |
| rclone | Free |
| **Total** | **~€16/month** |

This covers genuine irreplaceable data. The mainstream Plex library is
accepted as recoverable-but-annoying — Steve's drives are best-effort
fire insurance for it, not a guaranteed restore SLA.

---

## Secrets & Encryption

- rclone crypt passphrase: stored in KeePass, **never in any script or repo**
- B2 application key: stored in KeePass, injected via environment variable at runtime
- rclone config file location: `C:\Users\sandr\.config\rclone\rclone.conf`
  (contains encrypted credentials — back this up to B2 as well, bootstrapping caveat noted)

**Bootstrapping caveat:** The rclone config itself needs to be backed up somewhere
accessible without rclone already configured — print it or store in KeePass as text
so a bare-metal restore is possible.

---

## Next Steps

- [ ] Upgrade to Wien Energie SuperSchnell 1000 (prerequisite for practical seeding)
- [ ] Create Backblaze B2 account and bucket
- [ ] Generate B2 application key with write-only permissions for backup bucket
- [ ] Install rclone on Goliath, configure b2 + crypt remotes
- [ ] Run initial manual seed (~2TB irreplaceable data)
- [ ] Set up Task Scheduler nightly job
- [ ] Verify restore works (restore one file from B2 to confirm decrypt works)
- [ ] Set up Tailscale on Steve's machine for future delta sync of Plex content
- [ ] Document Steve's hardware and check drive health annually

---

## Related

- `integrations/vastai-gpu-hosting.md` — Vast.ai hosting shares the uplink; backup
  jobs and Vast transfers should not compete; schedule backup at 03:00 when Vast
  utilization is lower
- `integrations/salad-gpu-sharing.md` — same uplink sharing consideration
- `operations/WEBAPP_PORTS.md` — unrelated but same ops folder
- Wien Energie SuperSchnell 1000 upgrade — see ISP notes (no dedicated doc yet)
