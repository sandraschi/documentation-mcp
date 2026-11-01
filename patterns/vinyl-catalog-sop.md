# Vinyl Catalog SOP — The Shed Project

**Goal**: Catalog 3,000 vinyl records in a weekend, with AI categorization, RAG search, and Plex cross-reference.

## Hardware

| Item | Purpose |
|------|---------|
| Smartphone camera | Photo capture |
| Tripod + phone mount | Consistent framing (same height, angle, lighting) |
| Daylight LED lamp | Consistent lighting (avoid color cast) |
| Flat mat with marked zones | Frame guide for sleeve (left) and label (right) |
| Laptop with this repo | Processing pipeline |

## Photo Workflow (the weekend)

One vinyl → two photos → put back. 14 seconds per vinyl. 3,000 × 14s = ~12 hours (one good day with a friend.)

### Photo naming convention

Drop photos into `D:\Vinyl\inbox\`:

```
0001_sleeve.jpg     # Front cover, flat on mat
0001_label.jpg      # Vinyl label (side A, or whichever side is up in the sleeve)
0001_label_b.jpg    # Vinyl label side B (optional)
0002_sleeve.jpg
0002_label.jpg
...
```

### Shot guide (printable)

```
┌──────────────────────────────┐
│         MAT LAYOUT           │
│                              │
│  ┌──────────┐  ┌──────────┐  │
│  │ SLEEVE   │  │ LABEL    │  │
│  │ (front)  │  │ (12" or  │  │
│  │          │  │  7" vinyl│  │
│  │   A4     │  │  on mat) │  │
│  │  region  │  │          │  │
│  └──────────┘  └──────────┘  │
│                              │
│  Lighting: LED from top-left │
│  Camera: phone on tripod     │
│  above, centered             │
└──────────────────────────────┘
```

## Processing Pipeline

### Step 1: OCR (Tesseract)

```python
import pytesseract
from PIL import Image

def ocr_vinyl(path: str) -> dict:
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return {"raw_text": text, "file": path}
```

Tesseract is already available (CUA smoke test standard requires it at `C:\Program Files\Tesseract-OCR\tesseract.exe`).

### Step 2: AI categorization (Ollama)

```python
async def categorize(ocr_text: str) -> dict:
    prompt = f"""From this OCR text of a vinyl record sleeve/label, extract:
- artist
- album_title
- catalog_number
- year (estimate if not visible)
- genre (techno, house, rock, jazz, classical, etc.)
- side (A or B)
- speed (33, 45, 78)

Return ONLY valid JSON.

OCR text:
{ocr_text}
"""
    r = await httpx.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2:3b", "prompt": prompt, "stream": False
    })
    return json.loads(r.json()["response"])
```

### Step 3: Database + RAG

```sql
CREATE TABLE vinyl (
    id INTEGER PRIMARY KEY,
    sequential INTEGER UNIQUE,
    artist TEXT,
    album_title TEXT,
    catalog_number TEXT,
    year INTEGER,
    side TEXT,
    speed INTEGER,
    genre TEXT,
    era TEXT,
    mood TEXT,
    energy INTEGER,  -- 1-10
    sleeve_path TEXT,
    label_path TEXT,
    label_b_path TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

Vector embeddings via sentence-transformers for RAG search:
```sql
-- Query: "find me deep house for a wedding reception, 120 BPM vibe"
SELECT artist, album_title, genre, energy
FROM vinyl
ORDER BY embedding <-> query_embedding
LIMIT 10;
```

### Step 4: Plex cross-reference

```python
async def crossref_plex(artist: str, album: str) -> dict:
    r = await httpx.get(f"http://127.0.0.1:10856/api/search?q={artist} {album}")
    return r.json()  # {"found": true, "file_path": "..."}
```

## One-Liner (after photos are taken)

```powershell
python catalog.py D:\Vinyl\inbox\
```

Processes all unprocessed images, OCRs, categorizes, stores to SQLite, generates embeddings, reports progress with estimated time remaining.

## MCP Tool: `mixx_vinyl`

Add to `mixx-dj-mcp`:

| Operation | Params | Description |
|-----------|--------|-------------|
| `catalog` | `directory` | Process all unprocessed photos in directory |
| `search` | `query`, `genre`, `era`, `limit` | Search vinyl database with RAG |
| `gig_pick` | `query`, `count` | Pick N vinyls for a gig from a natural language description |
| `crossref` | `vinyl_id` | Find matching digital copy in Plex |
| `stats` | — | Total cataloged, genre distribution, era breakdown |
