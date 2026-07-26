# Grey Tools

Reference catalog of tools/libraries encountered during fleet work that
are legitimate, functional, and often well-maintained -- but that do
something ethically or legally borderline enough to warrant a second
look before adopting, rather than reaching for by default. Not a
blocklist. The point is: know they exist, know what they actually do,
decide deliberately each time rather than by habit.

---

## pycookiecheat

**What it does:** decrypts and reads cookies straight out of Chrome's
(or Firefox's) local encrypted cookie store -- on Windows via DPAPI,
macOS via Keychain, various Linux keyrings. Legit, actively maintained,
on PyPI, MIT-ish license, widely used as a building block.

**Why it's grey:** the cookie store it reads holds live session auth
for every site you're logged into. A script that calls
`chrome_cookies(url)` for one domain has, at that point, the technical
capability to read cookies for any domain in the same profile. The
library itself doesn't misuse this -- but anything built on it inherits
"can read your entire browser's live sessions" as its blast radius,
even if it only ever asks for one domain. cf. `press-auth` in the
`cli-printing-press` ecosystem, which uses this exact pattern (with
this library as a documented fallback) to auto-import live Chrome
session cookies for account-scoped CLI commands (Booking.com trips,
eBay bidding, LinkedIn, etc.) via `<tool> auth login --chrome`.

**Fleet stance:** don't default to this. Where account-scoped access
to a third-party site is genuinely needed, prefer an isolated,
dedicated browser profile the user logs into once by hand (see
`travelprep-mcp`'s `auth/booking_session.py` for the pattern) -- same
end result (a persisted session) without ever touching the encrypted
store of a browser profile used for anything else.

## cli-printing-press / printing-press-library (mvanhorn)

**What it does:** a large, actively-developed catalog (`registry.json`
lists 100+ entries) of "agent-native" Go CLIs, each generated from
browser-captured traffic against a real site/API, installed via
`npx -y @mvanhorn/printing-press-library install <name>`. Covers
travel, commerce, productivity, social -- e.g. `booking-com-pp-cli`,
`airbnb-pp-cli`, `ebay-pp-cli`. Real project, real GitHub activity, not
a scam as far as surface research showed.

**Why it's grey:** the auth-required half of nearly every CLI in the
catalog uses the live-Chrome-cookie-import pattern above
(`requires_browser_cookie_for_auth_endpoints` shows up constantly in
their generation metadata). Installing one of these means trusting a
third-party Go binary with your live session for that site, and by
construction (shared cookie-store access) technically with everything
else in that browser profile too. Also: much of what these CLIs do
(authenticated scraping of `mytrips.html`-style account pages,
evading bot detection on search) sits in the same ToS grey zone
Booking.com's own bot-detection is actively fighting against -- see
`hotelzero` below.

**Fleet stance:** fine to read for design ideas (this is where the
`travelprep-mcp` account-tool design was filched from), not something
to `npx install` and point at a live account without deliberately
deciding to accept the cookie-sharing risk.

## hotelzero / Playwright-based scrapers generally

**What it does:** `insprd/hotelzero`, already wrapped in
`travelprep-mcp`, drives a real Chromium instance via Playwright with
UA rotation and retry/backoff specifically to search Booking.com
without an API key.

**Why it's grey:** Booking.com actively fingerprints and blocks this
(confirmed live, 2026-07-14 -- see `travelprep-mcp` README). Automated
scraping of a site that's actively trying to detect and block automation
is a ToS violation in the fine print of most travel/commerce sites,
even for read-only, personal-use, no-resale usage. Low practical
enforcement risk for a single individual's low-volume personal
searches; not zero.

**Fleet stance:** acceptable for search/browse (no account involved,
no ToS-adjacent account-security risk), already in production use in
`travelprep-mcp`. Don't scale it up (no loops, no scheduled polling)
and don't extend the same pattern to anything account-authenticated
without the isolated-profile design above.

---

*Started 2026-07-14 during travelprep-mcp's Booking.com account-tool
build. Add entries here whenever fleet research surfaces another tool
in this category, rather than letting the knowledge evaporate at the
end of the chat that found it.*
