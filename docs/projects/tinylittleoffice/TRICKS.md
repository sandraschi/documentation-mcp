# TinyLittle tricks — a steal-this cookbook

How to build a **tinylittle-something**: fragment-only docs, sealed docs, short links,
hand-written links, and headless `lint`/`measure`. All paths are in the read-only
mirror `D:\Dev\repos\_upstream\tinylittleoffice`.

Design motto (upstream, Paul): *"The note passed in class. The note is the thing,
not a reference to something kept elsewhere."*

---

## Trick 1 — The document is the fragment

```
https://tinylittleoffice.com/<app>/#/v1/<app>[.view]/<payload>[?d&s=&x=&lang=&show&text]
```

* Everything after `#` is never sent to any server (browser behavior). The host sees
  static-file requests only: path names the app (`/sheet/`), never the doc.
* `v1` = link format version (TLO text). Nothing older is read.
* `.view` = `pdf/docx/csv/ics/embed/show…` — download on arrival or alternate showing.
* Query (all optional, all outside the payload): `?d` Display Link (read, don't edit),
  `?d&text` its words reflowed, `?show` deck opens presenting, `?s=<id>&x=<exp>`
  arrived-by-short-link banner, `?lang=` language choice.
* `Referrer-Policy: no-referrer` so following a link out never carries the doc address.
* `siteOf()` resolves the site root from any page, so the same build works at
  `/` and at `/tinylittleoffice/` (GitHub Pages mirror).

**Steal:** any "share by link, no backend" tool. Route = `#/v<ver>/<type>/<payload>`,
payload opaque to the router, all options in query. Keep the app/type name out of
the encrypted part only if you are fine leaking *which kind* of thing it is
(TLO leaks app id by design — tag does not cover it).

Refs: `src/kit/core/route.ts`, `docs/threat-model.md` ("The shape of it").

## Trick 2 — Pack smallest of three, with a frozen dictionary

`src/kit/core/codec.ts` (~180 lines, `fflate` only):

```
y<base64url(deflate_raw(utf8, DICTIONARY))>   # dictionary, usually wins
z<base64url(deflate_raw(utf8))>               # plain deflate
r<base64url(utf8)>                             # raw, wins for tiny docs
```

* `packDoc()` tries all three, keeps the shortest. `unpackDoc()` switches on the flag.
* Dictionary = frozen TLO-English + app words + markup (`DICTIONARY_TEXT`), 20–35%
  smaller on short docs. **FROZEN after v1:** new dict = new flag letter, never edit.
* `MAX_DOC_BYTES = 4MB` inflate cap — a small link unpacking to gigabytes is an attack.
* `URL_LIMIT = 2048` — the Share dialog's meter (IE-era safe length; modern browsers
  allow ~1M+, but pasting through chats/mail does not).

**Steal:** `encode = flag + b64(deflate|raw)`, `decode` with a hard inflate cap.
Train your own dictionary over your own corpus (`npm run dictionary` pattern), freeze it.

## Trick 3 — Base64url with `~`, breaks with `+`

Standard base64url uses `-` for 62. TLO uses **`~`** (`B64 = A–Z a–z 0–9 ~ _`):

* `-` is a UAX #14 line-break opportunity — long links got cut when pasted through
  mail/chat. `~` is unreserved in URIs and breaks nowhere. Reading accepts `-` too,
  so old links keep opening.
* `withBreaks()`: `+` after every 300 chars. iMessage/Signal won't linkify a run of
  >301 letters+digits; `+` is not in the alphabet, is fragment-legal, and is *not*
  a break opportunity — iMessage treats it as the break. Stripped before decode;
  links without breaks read the same.

**Steal:** if your tokens live in pasted text, avoid `-` and insert a non-alphabet
separator at the linkifier's limit. Lenient readers (accept old alphabet, ignore
separators) cost 3 lines and save every old link.

## Trick 4 — Sealed docs: app-made password, one HKDF pass, fresh IV per edit

`src/kit/share/crypt.ts` (~100 lines) + `docs/crypto/password.md`:

```
E + base64url( salt[16] | iv[12] | AES-256-GCM(key, iv, flag | packed_bytes) )
```

* Plaintext = 1 codec flag byte + packed bytes. Tag authenticates the flag too.
* Key: `HKDF-SHA256(ikm = NFKC(password).utf8, salt = 16 random bytes,
  info = "tinylittleoffice sealed v1", 32 bytes)` → non-extractable AES-GCM key.
  NFKC so full-width/changed-form typing still opens.
* No stretching (no scrypt/Argon2) **on purpose**: every password is app-made,
  20 chars from a 56-char alphabet (no `l I 1 o O 0`), rejection-sampled,
  `xxxx-xxxx-xxxx-xxxx` (dashes part of it) = **116 bits**. `2^116` offline guesses
  is infeasible; stretching would cost phones ~1s/open for nothing.
  `seal: true` makes the password and returns `{ url, password }`; a handed-in
  `password` is refused with `PASSWORD_REFUSED`.
* Fresh 12 B IV per seal (every edit re-seals, same key+salt). Safe to ~2^32 seals.
* Wrong password ≡ truncated link (GCM tag fail) — UI says both ("wrong password,
  or link was cut — ask for it again"). Key kept in memory for the visit;
  password never stored. Library keeps sealed payloads with no title/first-words.
* Floor: `E` + 60 chars for an empty doc (45 bytes). No version byte inside —
  `E` says the format, `v1` in the route is outside the tag.

**Steal:** for shareable secrets, generate the password yourself, one fast KDF pass,
random salt per secret + fresh IV per edit, authenticate your format flag. Tell users
to send password and link by *different* channels — same message = no protection.
Test vectors pattern: `test/vectors/password.json` + `test/crypto-vectors.test.ts`
(check kit output against hand-rolled WebCrypto).

## Trick 5 — Short links: ciphertext on the server, key in the fragment

`src/kit/share/short.ts` + `tinier/` (whole service logic ≈ 1 file) +
`docs/crypto/short-links.md`:

```
https://tinier.tinylittleoffice.com/<id>#<key>
POST /api {c, iv, ttl} → 201 {id, exp}      # ttl ∈ 1h/1d/1w/1m, default 1w
GET  /api/<id>         → {c, iv, exp}       # 404 once gone
```

* Plaintext = long-link UTF-8. Per-link 32 B key + 12 B IV, AES-256-GCM, key only in
  `#`. Server stores `{id (7 chars, ~35 bits), c (≤16KB b64), iv, exp}` in D1.
  It sees length + timing, never content.
* Immutable + expiring: no update, no delete, swept hourly + on read-after-expiry.
  D1 Time Travel can resurrect rows briefly — still ciphertext.
* Anti-abuse without identity: per-address-per-day counter under
  `sha256(BRAKE_KEY \n day \n address)`, 100/day, refused with 429. Counts live ≤2 days.
  No logs (`observability: false`, no `console.*`, held by `test/tinier.test.ts`).
* Arrival UX: `?s=<id>&x=<exp>` + "expires in N days" banner + "copy into a new
  document" (long link, never expires).

**Steal:** the shape `store(ciphertext) + fragment-key` upgrades any dumb KV store
into a zero-knowledge shortener. Copy the expiry/deletion/rate-limit trio with it.

## Trick 6 — Plain links: hand-writable, agent-writable

```
https://tinylittleoffice.com/<app>/#title=…&doc=<percent-encoded TLO>&by=…&lang=…
```

Longer than packed links, readable and writable by hand. Agents write these;
site + `api.js link()` write packed ones; both open. Rules agents break first
(`public/llms.txt`): keep every space/newline (`%20`/`+`, `%0A`), one slide = one
thing, commas split lists (write `2000` not `2,000`).

**Steal:** offer *two* encodings — packed (default, short) + plain (debuggable).
Agents and humans onboard through plain, production shares through packed.
`read()` accepts both (fragment or full URL).

## Trick 7 — Headless API: lint + measure instead of opening a browser

`src/api.ts` (served as `/api.js`, zero DOM, runs in page/Node 24/Deno/Bun) and
`packages/doc/` (npm `tinylittleoffice`, CLI `tinyoffice`/`tinylittleoffice`):

```js
import { link, read, lint, measure } from 'https://tinylittleoffice.com/api.js';
link('sheet', 'Item | Cost:money\n--- | ---\nRent | 1200\n', { title: 'Budget' });
read(url);            // { app, view, text, json, title, by, display, lang }
await lint(app, text);    // findings with app/slide/block/kind/words/fix
await measure(app, text); // layout numbers: headline px/lines/cut, overflows
```

* `lint`/`measure` read the *same layout code that draws pages* — check docs without
  opening them. Fenced inner docs are linted too.
* `toJson`/`fromJson` round-trip kernel `Doc` ↔ canonical TLO ↔ JSON Schema
  (`packages/doc/schema/tlo.schema.json`, generated from types — stale schema fails tests).
* CLI: `shapes <app>` (what it reads), `example <app> [shape]` (smallest doc per
  shape, cut from templates — byte-identical), `try <app> file` (lint+measure+json),
  `link/read/file/diff/lint/measure`, `skill --into ~/.claude/skills`.
* `compare(a, b)` = block diff (`{ same, removed, added, changes }`).
* Budgets: `/api.js` size gated (`budgets.json`); app defs stay light (no DOM/
  templates in registry — lazy `templates()`/`editor()` imports; `vite.api.config.ts`
  leaves editors out).

**Steal:** ship three surfaces from one kernel — interactive site, URL-importable
module, zero-dep CLI — and make the *checker* (`lint`) use the *renderer*, so agents
never need a browser. Pin it with corpus tests (`write(parse(x)) === x` over every
template/example) + grammar fuzz (`test/doc/properties.test.ts`) + browser walks.

---

## Minimal reimplementation (pseudo-TS, ~60 lines of real logic)

```ts
// 1. payload
const B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~_';
encodeDoc = (doc) => !doc ? '' : best('r', raw, 'z', deflate(raw), 'y', deflate(raw, FROZEN_DICT));
decodeDoc = (p) => !p ? '' : unpack(p[0], fromB64(p.slice(1).replace(/\+|%2B/gi, '')));
// 2. route
link = (app, doc, site) => `${site}${app}/#/v1/${app}/${withBreaks(encodeDoc(doc))}`;
// 3. sealed
seal = async (pw) => 'E' + toB64(salt16 | iv12 | AES_GCM(HKDF(NFKC(pw), salt, INFO), iv, flag | packed));
// 4. short
short = async (longUrl) => { POST(store, AES_GCM(randKey, randIV, longUrl)); return `${store}/${id}#${key}`; };
```

Swap `deflate` for any compressor, keep: frozen dictionary + inflate cap, `~` + `+`
rules, `E` marker, HKDF info string, per-secret salt + per-edit IV, key-in-fragment.

## What NOT to copy (it will bite)

* Don't render user HTML/CSS/JS from a link on your own domain (upstream removed the
  app that did — phishing kit with your domain). TLO has no picture/embed kind;
  `![alt](url)` reads as link text. Documents never run code, never fetch (except
  Trip map tiles, behind a switch, direct to provider, no referrer).
* Don't log link creation/opening, don't add analytics/fonts/CDN scripts — every host
  must come from one list (`src/kit/core/network.ts` → `docs/network.md` + CSP,
  held by tests). Two Cloudflare dashboard script-injectors stay off (Web Analytics,
  Bot Fight Mode JS).
* Don't let users pick weak passwords. Generate them. Don't store them — hold the
  derived non-extractable key in memory only.
* Don't "improve" the dictionary. Freeze it; new compression = new flag.
